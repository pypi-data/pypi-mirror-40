## gugfug-ci
simple continues integration tool

#### You can run gugfug-ci using docker run command with -v flag like

```shell
docker run -v <path_to_your_folder_that_contain_config_files>:/etc/gugfug-ci/conf.d gugfug-ci
```

#### Your config folder may contain following files:
  - ci.conf.py
  - gunicorn.conf.py
