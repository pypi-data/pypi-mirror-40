# nwpc-workflow-model

[![Build Status](https://travis-ci.org/perillaroc/nwpc-workflow-model.svg?branch=master)](https://travis-ci.org/perillaroc/nwpc-workflow-model)
[![codecov](https://codecov.io/gh/perillaroc/nwpc-workflow-model/branch/master/graph/badge.svg)](https://codecov.io/gh/perillaroc/nwpc-workflow-model)

The workflow model using in NWPC, supports SMS and ecFlow.

## Introduction

In NWPC, we run tasks using a workflow software, such as SMS and ecFLow by ECMWF.
`nwpc-workflow-model` is designed to bring a workflow model into our programs.

## Components

### SMS
 
Please see [nwpc_workflow_model/sms/README.md](nwpc_workflow_model/sms/README.md) for more information.

### ecFlow

Same as SMS.

## Getting Started

Download the latest source code from Github and install `nwpc-workflow-model` using:

```bash
python setup.py install
```

## Tests

Install packages for test using `pip install .[test]`.

Use `pytest` to run tests.

## License

Copyright &copy; 2016-2019 Perilla Roc.

`nwpc-workflow-model` is licensed under [The MIT License](https://opensource.org/licenses/MIT).
