import slack
import os

slack_token = os.environ["SLACK_API_TOKEN"]
client = slack.WebClient(token=slack_token)


def sendMessSlack(chaine,mess):
	client.chat_postMessage(
  	channel=chaine,
  	text=mess
	)