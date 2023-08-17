# vcrpy-boilerplate

While [vcrpy](https://vcrpy.readthedocs.io/en/latest/) is very powerful, it can be difficult
to use out-of-the-box. This boilerplate wraps `vcrpy` with some useful features and
shows examples of how to quickly record and replay cassettes in unit tests.

While examples in this project are written with `unittest`, this code can easily be adapted to
`pytest` or any other use case.

Key features:
- Uses environment variables to determine record vs. replay mode
- Easily mock intermittent errors and hard-to-reproduce responses alongside cassettes
- Configurable global settings for common settings (e.g. always discard noisy HTTP headers)
- Separates simulation usage from how it is defined to allow easy changes in the future

# Running Examples

In order to run this project, you will need to install the project requirements.

```
pip install -r requirements.txt
```

To see how this project works, it is recommended that you attempt to record all cassettes used
by this project. To do this, simply run all tests in the `examples/` with the `CASSETTE_MODE`
environment variable set to `record`.

```
export CASSETTE_MODE=record
python -m unittest discover examples   
```

This will run all tests and record all HTTP requests in the created `cassettes/` folder. Next,
run all tests in playback mode by setting `CASSETTE_MODE` to `playback` and running tests again.

```
export CASSETTE_MODE=playback
python -m unittest discover examples   
```

This time no HTTP requests were ran, and instead the HTTP requests recorded in the `cassettes/`
folder were used to replay tests.

# Recommended Process

When developers are writing new tests, they should use `record` mode to use real HTTP requests.
Once the tests are written, they should be committed to the git repository alongside the tests.
This means that anyone who runs the tests in `playback` mode will use cassettes instead of 
real HTTP requests, which means the tests will reliably run in any environment.