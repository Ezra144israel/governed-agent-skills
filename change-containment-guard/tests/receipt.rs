use change_containment_guard::{check_receipt, run_verification, seal_contract};
use serde_json::json;
use std::fs;
use std::process::Command;
use tempfile::TempDir;

fn git(repo: &TempDir, args: &[&str]) {
    assert!(
        Command::new("git")
            .current_dir(repo.path())
            .args(args)
            .status()
            .unwrap()
            .success()
    );
}

fn setup() -> (TempDir, TempDir, std::path::PathBuf) {
    let repo = TempDir::new().unwrap();
    let evidence = TempDir::new().unwrap();
    git(&repo, &["init", "-q"]);
    git(&repo, &["config", "user.email", "test@example.invalid"]);
    git(&repo, &["config", "user.name", "Test"]);
    fs::write(repo.path().join("main.txt"), "base\n").unwrap();
    git(&repo, &["add", "."]);
    git(&repo, &["commit", "-qm", "base"]);
    let contract_path = evidence.path().join("contract.json");
    let contract = json!({
        "schema": "change-containment-contract/v1",
        "repository_id": null,
        "baseline": null,
        "rules": [{"class":"implementation","patterns":["main.txt"],"allow_staged":true,"allow_unstaged":true,"allow_kinds":["file"],"allow_test_suppression":false}],
        "dependency_patterns": [], "generated": [], "test_ecosystems": [],
        "unknown_test_patterns": ["tests/**"],
        "verification_commands": [["git", "diff", "--check"]],
        "contract_hash": null
    });
    fs::write(
        &contract_path,
        serde_json::to_vec_pretty(&contract).unwrap(),
    )
    .unwrap();
    seal_contract(&contract_path, repo.path()).unwrap();
    (repo, evidence, contract_path)
}

#[test]
fn receipt_rejects_post_green_mutation_and_cross_repository_reuse() {
    let (repo, evidence, contract_path) = setup();
    fs::write(repo.path().join("main.txt"), "allowed\n").unwrap();
    let receipt_path = evidence.path().join("receipt.json");
    let receipt = run_verification(
        &contract_path,
        &receipt_path,
        repo.path(),
        &["git".into(), "diff".into(), "--check".into()],
    )
    .unwrap();
    assert_eq!(receipt.exit_status, 0);
    check_receipt(&contract_path, &receipt_path, repo.path()).unwrap();

    fs::write(repo.path().join("main.txt"), "mutated after green\n").unwrap();
    assert!(check_receipt(&contract_path, &receipt_path, repo.path()).is_err());

    let other = TempDir::new().unwrap();
    git(&other, &["init", "-q"]);
    assert!(check_receipt(&contract_path, &receipt_path, other.path()).is_err());
}

#[test]
fn unapproved_verification_command_is_rejected() {
    let (repo, evidence, contract_path) = setup();
    let receipt_path = evidence.path().join("receipt.json");
    assert!(
        run_verification(&contract_path, &receipt_path, repo.path(), &["true".into()],).is_err()
    );
}

#[test]
fn receipt_rejects_cross_branch_contract_replacement_and_receipt_corruption() {
    let (repo, evidence, contract_path) = setup();
    let receipt_path = evidence.path().join("receipt.json");
    run_verification(
        &contract_path,
        &receipt_path,
        repo.path(),
        &["git".into(), "diff".into(), "--check".into()],
    )
    .unwrap();

    let base_branch = Command::new("git")
        .current_dir(repo.path())
        .args(["branch", "--show-current"])
        .output()
        .unwrap();
    let base_branch = String::from_utf8(base_branch.stdout).unwrap();
    git(&repo, &["checkout", "-qb", "other"]);
    assert!(check_receipt(&contract_path, &receipt_path, repo.path()).is_err());
    git(&repo, &["checkout", "-q", base_branch.trim()]);

    let original_contract = fs::read(&contract_path).unwrap();
    let mut changed: serde_json::Value = serde_json::from_slice(&original_contract).unwrap();
    changed["verification_commands"] = json!([["true"]]);
    fs::write(&contract_path, serde_json::to_vec_pretty(&changed).unwrap()).unwrap();
    assert!(check_receipt(&contract_path, &receipt_path, repo.path()).is_err());
    fs::write(&contract_path, original_contract).unwrap();

    let mut receipt: serde_json::Value =
        serde_json::from_slice(&fs::read(&receipt_path).unwrap()).unwrap();
    receipt["output_digest"] =
        json!("sha256:0000000000000000000000000000000000000000000000000000000000000000");
    fs::write(&receipt_path, serde_json::to_vec_pretty(&receipt).unwrap()).unwrap();
    assert!(check_receipt(&contract_path, &receipt_path, repo.path()).is_err());
}
