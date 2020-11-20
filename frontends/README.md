# frontends

## Project setup

### Download and install pre-requisite.

#### Google API and Access.

_Because i'm develop this application in Windows 10. So this instruction will cover only Windows 10 OS._

```bash

choco install gcloud

# enable alpha API.
gcloud init 
gcloud auth login
gcloud alpha services api-keys # If you not enable alpha before you will need to do following step ( little effort ).  

# Create Project

$project_name="project-scg-test-exam00"
gcloud alpha projects create --name=$project_name
$project_id=$(gcloud alpha projects list | Select-string -Pattern $project_name).Line.split()[0]
gcloud alpha services api-keys create --project $project_id

# Output will showing like this 
Operation [operations/akmf.9cb38925-35f5-443a-a2e2-e6c98b7e4337] complete. Result: {
    "@type":"type.googleapis.com/google.api.apikeys.v2alpha1.ApiKey",
    "createTime":"2020-11-18T16:26:13.260365Z",
    "keyString":"xxxxxxxxxxxxxxxxxxxxTRMHmIFPS1yIfTw",
    "name":"projects/99999999999/keys/586fa3cc-b0e4-4e08-1111-99999999999",
    "state":"ACTIVE",
    "updateTime":"2020-11-18T16:26:13.368570Z"
}
# Then copy key string 
# Delete project.
gcloud alpha projects delete $project_name
See https://cloud.google.com/resource-manager/docs/creating-managing-projects for information on shutting down projects






```


```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
