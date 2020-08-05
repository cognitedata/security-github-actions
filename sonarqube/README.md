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

## Example usage

uses: actions/sonarqube@v1
with:
  project_path: '/path-to-project/'
  sonarqube_host: 'sonarqube.example.com'
  iap_client_id: '123-example.apps.googleusercontent.com'
