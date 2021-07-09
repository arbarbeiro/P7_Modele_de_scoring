# How to deploy an app to Heroku platform as a service (PaaS)

1. Create a new folder for your project and initialize it with git. 
```
$ git init
```
2. Create a virtualenv with python's module venv(python3) or virtualvenv(python2), or with conda (but use pip):
```
$ python3 -m venv venv_name
# or
$ virtualenv venv_name

# activate the virtualenv
$ source venv_name/bin/activate 
```

3. Reinstall your app's dependencies with this virtualenv:

```
pip install dash
pip install plotly
etc.
```

You will also need a new dependency, gunicorn, for deploying the app:
```
$ pip install gunicorn
```

Keep the rest of the steps from step3 in the [dash website](https://dash.plotly.com/deployment) (including an example of dash app). 

---------------------------
### Creating the new app in keroku

1. Install Heroku Command Line Interface (CLI). CLI is used to manage and scale your applications, provision add-ons, view your application logs, and run your application locally.
> In Ubuntu:
>```
>$ sudo snap install heroku --classic
>```
>See [here](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) for windows.

2. Use the `heroku login` command to log in to the Heroku CLI.
```
$ heroku login
```

3. Initialize Heroku, add files to Git, and deploy
```
$ heroku create app_name # app_name should be a unique name
$ git add . # add all files to git
$ git commit -m 'Initial app app_name'
$ git push heroku master # deploy code to heroku
$ heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
```
_The app should be visible at https://app_name.herokuapp.com_

Add a remote to your local repository or confirm that a remote named `heroku` has been set for your app:
```
$ heroku git:remote -a app_name
or
$ git remote -v
```
> Note: By default, the Heroku CLI names all of the Heroku remotes it creates for your app heroku, so you can rename your remote using:
>```
>$ git remote rename heroku 
>heroku-staging
>```

4. To update the app, use the git commands as usual and push it to keroku master (`git push heroku master`)
