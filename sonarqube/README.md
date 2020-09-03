# SonarQube code scan Docker action

This action runs a SonarScanner and reports to a centralized server.

## Inputs

### `project_path`

**Optional** The path to the file or directory to scan with SonarScanner. Default `"."`.

### `sonarqube_host`

The hostname of the sonarqube instance.

### `sonarqube_token`

API Token to authenticate with the SonarQube instance.

### `aad_tenant`

AAD tenant.

### `iap_client_id`

Client ID of the app registered with Microsoft identity platform.

### `iap_client_secret`

Client secret to use for authentication when requesting an IAP token.

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
  aad_tenant: ${{ secrets.AAD_TENANT }}
  iap_client_id: ${{ secrets.IAP_CLIENT_ID }}
  iap_client_secret: ${{ secrets.IAP_CLIENT_SECRET }}
  pr_source_branch: ${{ github.head_ref }}
  pr_target_branch: ${{ github.base_ref }}