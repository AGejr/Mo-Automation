# Mo-Automation

### What is Mo Automation
Mo Automation is an addition to the default Github projects automation, it is designed with small development teams in mind.
Traditional project management software such as Jira can be a bit too heavyweight for small teams. 
Therefore this project tries to minimize the amount of different software tools a small development team has to utilize
by adding more functionality to the default Github projects automation.

### Target group
The target group of this tool is small development teams such as project groups consisting of computer science students. 
The tool is especially useful when learning how to use Github since it nudges the user to use many of Github's features.  

### The purpose of Mo Automation
The aim of this project is to automate project management so that developers don't have to manually drag and drop project cards.
With this tool, it should be possible to go through the process of implementing an issue exclusively by interacting with an issue.

## Table of contents
1. [Installation](#Installation)
2. [Detailed usage](#Detailed-usage)
3. [Configuration](#Configuration)
    * [Project board name](#Project-board-name)
4. [Planned features](#Planned-features)
    * [Finish main functionality](#Finish-main-functionality)
    * [Testing](#Testing)
    * [Discord bot integration](#Discord-bot-integration)

## Installation

* Create .github/workflows folder in repository root folder
* Create a file named mo-automation.yml in the .github/workflows folder
* Add the contents of the code block below to the mo-automation.yml file

```
on:
  issues:
    types: [ opened, assigned, milestoned ]
  pull_request:
    branches: [ main ]

jobs:
  create_automation_job:
    runs-on: ubuntu-latest
    steps:
      - name: Process event
        uses: AGejr/Mo-Automation@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PROJECT_BOARD_NAME: Automated Board
```

## Detailed usage

* Follow the installation instructions above
* Create the first issue
  * It's important that you **_only_** give the issue a title (and a optional description)
  * If a board with the default name couln't be found, a new project board is automatically created 
    * The issue will be added to the 'Backlog' column in the project board
* (Some time might pass until the issue is relevant)
* If you use sprints, or something similar, create it as a milestone
  * (You should be using short term deadlines, however but if you don't, go ahead and move the issue to 'To Do')
* When the issue becomes relevant, add it to the milestone
  * The issue is automatically moved to 'To Do'
* When you are ready to begin implementing the issue, assign a assignee to the issue
  * The issue is automatically moved to 'In Progress'
  * Furthermore, a branch named after the issue will be created
    * (The naming convention is issue-\<issue number\>-\<underscore seperated issue title\>)
* When you are done implementing the issue, create a pull request
  * ~~The issue is automatically moved to 'In Review'~~
  * ~~Request a review~~
    * ~~The reviewer should look through the changes and request changes if anything needs to be changed~~
    * ~~(At this point you shouldn't need to apply large changes to your branch, only minor)~~
* ~~When the reviewer approves your branch, go ahead and merge it with master~~
  * ~~The branch is automatically deleted and the issue is moved to 'Done'~~

(Strikethrough part is not implemented yet)

## Configuration

### Project board name

The project board name can be configures to your liking by changing the PROJECT_BOARD_NAME property in the mo-automation.yml file.

## Planned features

### Finish main functionality

The rest of the main functionality should be implemented. In in continuation of that, the app should be released to Github marketplace.

### Testing

Tests should be implemented to ensure functionality.

### Discord bot integration

It would be nice to have a bot that creates a notification in a discord channel when a pull request requires a review.


