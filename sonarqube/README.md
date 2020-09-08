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
<<<<<<< HEAD
<<<<<<< HEAD

### `iap_service_account`
  
Service account credentials for SonarQube IAP.
=======
>>>>>>> b8018cfb3913c6bff0c09aaab21382d5a3a1fdfa
=======
>>>>>>> b8018cfb3913c6bff0c09aaab21382d5a3a1fdfa

### `api_key`

API key used to access Google APIs.

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
  iap_client_id: ${{ secrets.IAP_CLIENT_ID }}
<<<<<<< HEAD
<<<<<<< HEAD
  iap_service_account: ${{ secrets.IAP_SA }}
=======
>>>>>>> b8018cfb3913c6bff0c09aaab21382d5a3a1fdfa
=======
>>>>>>> b8018cfb3913c6bff0c09aaab21382d5a3a1fdfa
  api_key: ${{ secrets.API_KEY }}
  pr_source_branch: ${{ github.head_ref }}
  pr_target_branch: ${{ github.base_ref }}