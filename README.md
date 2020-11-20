# Sample Application use Flask with Vuejs.

This project (firstly) intend to use for interview test. However i found this can practice my self for full-stack dev 
as well. So this project will continue even i met a dead-line commit. 

## Dead-line  commit
* midnight 20/11/2020. (_**Fail**_)

## State 
* NOT complete yet at all. 

## Install and Config.
TODO.

## Feature
### Backend.
- [ ] Please use “Google API” for finding the best way to go to Central World from SCG Bangsue.
- [x] X, Y, 5, 9, 15, 23, Z  - Please create a new function for finding X, Y, Z value.
- [ ] If A = 21, A + B = 23, A + C = -21 - Please create a new function for finding B and C value.
- [ ] Have unit test.
- [ ] API caching.
- [ ] Queueing jobs and processing them in the background with workers for scalability.
- [x] Monitoring worker task.
- [ ] Implement by using for [Flask blue-print instead.](https://flask.palletsprojects.com/en/1.1.x/blueprints)
- [ ] Oauth Authentication. ( will support role to query data., users allow.)
- [ ] JWT Token authentication for client.
- [ ] implement container environment for local ( docker-compose ) and Kubernetes chart deploy support.
- [ ] Add Golang backend support.
- [ ] Integrate with Auth0.

### Front-end.
- [ ] Create a new router called “DOSCG”.
- [ ] Please use Bootstrap V4 for CSS.
- [ ] Please create Top bar, body, and footer for every page components.
- [ ] Please create a new page for showing results from your API(separate router by each API)
- [ ] One simple static page for your CV.

### Thrid-Party. Application.
- [ ]  create a small project using Line messaging API for getting a notification when your Line Bot can not answer a question to the customer more than 10 second.

This application implement AWS Step-function with LINE Bot. that can control flow of timer for conversation as need.
 
## Frontend configure.
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
