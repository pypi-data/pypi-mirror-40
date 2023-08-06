![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# politico-civic-campaign-tracker

### Quickstart

1. Install the app.

  ```
  $ pip install politico-civic-campaign-tracker
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'tracker',
  ]

  #########################
  # tracker settings

  TRACKER_SECRET_KEY = ''
  TRACKER_AWS_ACCESS_KEY_ID = ''
  TRACKER_AWS_SECRET_ACCESS_KEY = ''
  TRACKER_AWS_REGION = ''
  TRACKER_AWS_S3_BUCKET = ''
  TRACKER_CLOUDFRONT_ALTERNATE_DOMAIN = ''
  TRACKER_S3_UPLOAD_ROOT = ''
  ```

### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd tracker/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/tracker"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```

### Slack Workflows

#### Changing A Candidate Rating

1. Type `/2020-rating` into any channel on Slack
2. Select the candidate's rating you want to change.
3. Select the new rating for that candidate.
4. Click save.

You should see a feedback message that confirms you successfully changed the rating.


#### Adding a Quote

1. Type `/2020-quote` in any channel on Slack.
2. Choose the candidate who said the quote
3. Enter the full text of the quote
4. Enter the date the quote was spoken
5. Optionally, enter the location of the quote (e.g., American University, Washignton, DC)
6. Optionally, Add a link to the quote (e.g., full text of a speech, video of the quote, etc.)

You should see a feedback message that confirms you successfully added the quote. The message will provide buttons to edit or delete the quote if an error was made.


#### Adding an endorsement

1. Type `/2020-endorsement` in any channel on Slack.
2. Choose the candidate who is being endorsed.
3. Enter who made the endorsement.
4. Enter the date the endorsement was made.
5. Enter the statement made about the endorsement, if there was one. If this is very long, choose a key quote.
6. Enter a link to the full endorsement.

You should see a feedback message that confirms you successfully added the endorsement. The message will provide buttons to edit or delete the quote if an error was made.

#### Adding a story

1. Type `/2020-story` in any channel on Slack.
2. Choose the candidate the story is about.
3. Enter the URL of the story.
4. Optionally, enter a custom description for this story to appear on our pages. By default, the page will show the social description.

You should see a feedback message that confirms you successfully added the story. The message will provide buttons to edit or delete the quote if an error was made.


#### Adding a video

1. Type `/2020-video` in any channel on Slack.
2. Enter the Brightcove ID of the video
3. Choose the candidate the story is about.
4. Enter the date the video was published.
5. Enter a headline for the video.
6. Enter a description for the video.

You should see a feedback message that confirms you successfully added the video. The message will provide buttons to edit or delete the quote if an error was made.


#### Ambiguous Tweet Is Tagged

 1. Message is posted in the `2020-tracker` Slack channel with:
  - A `@mention` to the reporter who tweeted the ambiguous tweet
  - The tweet in question
  - A dropdown list with all the active candidates


 2. Reporter or editor choses a candidate from the dropdown list.

 3. The dropdown is replaced with a sentence saying the tweet has been assigned to the specific candidate.


### Twitter Workflow

##### Getting on the whitelist

Ask the interactives team to get your Twitter handle on the whitelist of Twitter accounts that can tweet at our bot and get their content onto our pages.

##### Tweeting reportage at the bot

1. Write a tweet that includes the candidate's name and @-mentions the bot. Example:

> Beto O'Rourke will announce his candidacy today at a town hall in Austin, Texas. @tracking2020

That's it! The bot will retweet this tweet, and the tweet will be embedded on our Beto O'Rourke page.

Sometimes, we will be unable to determine what candidate the tweet is about. For example:

> Joe Biden attacked Bernie Sanders' free college plan as "naive, wishful thinking." @tracking2020

We don't know if this is about Joe Biden or Bernie Sanders. In that case, see the [ambiguous tweet is tagged docs](#ambiguous-tweet-is-tagged) above.

##### Candidate quotes via the bot

You can also quote tweets and leave comments on them in the quote. Just make sure you tag the bot and name the candidate.

> Kamala Harris announcing her support for universal basic income via Twitter is a sign of how campaigning has changed in the modern era. @tracking2020 https://twitter.com/KamalaHarris/status/1069638903378952193

This will embed your tweet and show the tweet you quoted.

Sometimes, a candidate will say something important on Twitter, and we want to send that quote in with no context. You can leverage the bot to do this quickly by quote tweeting the important tweet, and _only_ tagging the bot. For example:

> @tracking2020 https://twitter.com/CoryBooker/status/1068271280082886657

In this case, because no context was added, we will embed _just_ the quoted tweet on the page.

However, if you have time, we would prefer you use Slack to add this quote, because we can get more data about the quote from there. See [the docs](#adding-a-quote) above.