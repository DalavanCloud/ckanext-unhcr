# ckanext-unhcr

[![Build Status](https://travis-ci.org/okfn/ckanext-unhcr.svg?branch=master)](https://travis-ci.org/okfn/ckanext-unhcr)
[![Coverage Status](https://coveralls.io/repos/github/okfn/ckanext-unhcr/badge.svg?branch=master)](https://coveralls.io/github/okfn/ckanext-unhcr?branch=master)

CKAN extension for the UNHCR RIDL project

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Requirements](#requirements)
- [Setting up environment](#setting-up-environment)
- [Working with docker](#working-with-docker)
- [Starting development server](#starting-development-server)
- [Running unit tests](#running-unit-tests)
- [Running E2E tests](#running-e2e-tests)
- [Building static assets](#building-static-assets)
- [Working with i18n](#working-with-i18n)
- [Loging into container](#loging-into-container)
- [Updating readme](#updating-readme)
- [Managing docker](#managing-docker)
- [Reseting docker](#reseting-docker)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Requirements

This extension is being developed against CKAN 2.7.x

Please follow installation instructions of the software below if needed. Also, take a look inside the `Makefile` to understand what's going on under the hood:
- `docker`
- `docker-compose`
- `/etc/hosts` contains the `127.0.0.1 ckan-dev` line

For building static assets and running end-to-end tests Node.js is required and can be installed with these commands:

```bash
$ nvm install 10
$ nvm use 10
$ npm install
```

## Setting up environment

Clone the `ckanext-unhcr` repository (assuming that we're inside the `docker-ckan-unhcr/src` directory):

```bash
$ git clone git@github.com:okfn/ckanext-unhcr.git
$ cd ckanext-unhcr
```

It's designed to support live development of extensions. The only one requirement is that the folder with the project should be inside `docker-ckan-unhcr/src`. See `docker-ckan-unhcr` for more information.

## Working with docker

The whole docker setup is inside the `docker-ckan-unhcr` directory. You can tweak any CKAN instance's aspects there (e.g. patches/cron/etc). To add other CKAN extensions to the work - add its folders to `docker-compose.dev.yml` (see `ckan-dev` volumes).

Pull the latest `ckan-base/dev` images and build the project's images:

```
$ make docker
```

## Starting development server

Let's start the development server. It's recommended to run this command in an additional terminal window because you need it running during the work. All changes to connected extensions will trigger live-reloading of the server:

```bash
$ make start
# see CKAN logs here
```

Now we can visit our local ckan instance at (you can login using `ckan_admin@test1234`):

```
http://ckan-dev:5000/
```

## Running unit tests

We write and store unit tests inside the `ckanext/unhcr/tests`. Prefer to name test files after feature/bug names. To run the tests you should have the development server up and running:

```bash
$ make test
```

## Running E2E tests

We write and store E2E tests inside the `tests` directory. Prefer to name test files after feature/bug names. To run the tests you should have the development server up and running:

```bash
$ make e2e
$ npx nightwatch tests/<testname>.js # for a single E2E test
```

See the `how to write E2E tests` guide:
- http://nightwatchjs.org/guide

## Building static assets

Put your images/fonts/etc inside the `ckanext/unhcr/fanstatic` folder. It can be used as usual ckan `fanstatic` and `public` contents. At the same time, we use JS and CSS preprocessors to build. Put your scripts/styles inside the `ckanext/unhcr/src` and build it:

```bash
$ make assets
```

Processed styles will be put to the `ckanext/unhcr/fanstatic` folder.

## Working with i18n

To extract i18n messages and compile the catalog we have to have our development server running. In another terminal window run a command:

```
$ make i18n
```

See CKAN documentation for more on i18n management.

## Loging into container

To issue commands inside a running container:

```
$ make shell
```

Now you can tweak the running `ckan-dev` docker container from inside. Please take into account that all changes will be lost after the next container restart.

## Updating readme

To update this readme's table of contents run:

```bash
$ make readme
```

## Managing docker

There are a few useful docker commands:

```bash
$ docker ps -aq # list all containers
$ docker stop $(docker ps -aq) # stop all containers
$ docker rm $(docker ps -aq) # remove all containers
$ docker rmi $(docker images -q) # remove all images
```

## Reseting docker

> It will destroy all your projects inside docker!!!

If you want to start everything from scratch there is a way to prune your docker environment:

```
$ docker system prune -a --volumes
```
