# Sample Application use Flask with Vuejs.

This project (firstly) intend to use for interview test. However i found this can practice my self for full-stack dev 
as well. So this project will continue even i met a dead-line commit. (**midnight 20/11/2020**) 

## State 
* NOT complete yet at all. 

## Install and Config.


## Feature
### Backend.
- [x] Can fetch shortest distance by using Google MAP API. **Mandatory**.
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
- [x] Have Front-end that use VUEjs. ( locate at frontends folder)
- [ ] Support PWA ( Service-worker ) to caching all of data. **Mandatory**.

### Thrid-Party. Application.
- [ ]  create a small project using Line messaging API for getting a notification when your Line Bot can not answer a question to the customer more than 10 second.

This application implement AWS Step-function with LINE Bot. that can control flow of timer for conversation as need.
 
