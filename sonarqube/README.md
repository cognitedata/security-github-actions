# SonarQube code scan Docker action

This action runs a SonarScanner and reports to a centralized server.

## Inputs

### `project_path`

**Optional** The path to the file or directory to scan with SonarScanner. Default `"."`.

### `sonarqube_host`

The hostname of the sonarqube instance.

### `sonarqube_token`

API Token to authenticate with the SonarQube instance.

### `iap_client_id`

Client ID of OAuth provider used to get the IAP token.

### `iap_service_account`

Service account credentials for SonarQube IAP.

### `pr_source_branch`
Name of the source branch if triggered from PR.

### `pr_target_branch`
Name of the target branch if triggered from PR.

## Example usage

uses: actions/sonarqube@v1
with:
  project_path: '/path-to-project/'
  sonarqube_host: 'sonarqube.example.com'
  sonarqube_token: ${{ secrets.SONARQUBE_TOKEN }}
  iap_client_id: '123-example.apps.googleusercontent.com'
  iap_service_account: ${{ secrets.SONARQUBE_SERVICE_ACCOUNT }}
  pr_source_branch: ${{ github.head_ref }}
  pr_target_branch: ${{ github.base_ref }}
