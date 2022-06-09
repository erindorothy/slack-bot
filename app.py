import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import gitlab

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
gl = gitlab.Gitlab(private_token=os.environ.get("GITLAB_TOKEN"))
assert len(os.environ.get("GITLAB_TOKEN")) > 0
# Listens to incoming messages that contain "list project issues"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("list project issues")
def message_issues(message, say):
    # say() sends a message to the channel where the event was triggered
		issues = gl.issues.list()
		issue = issues[0]
		intro = "Listing all issues for the project.\n"
		msg = message['text']
		issueInfo = ""
		for i in range(len(issues)):
			issueInfo += (str)(i+1) + ". " + issues[i].title + " " + issues[i].assignee['name'] + " " +  issues[i].web_url + "\n"
		fmt = f"I heard you say: {msg} \n\n {intro} \n\n The issue title, assignee(s), and URL to the issue are: \n\n {issueInfo}."

		block = [{
			"type": "section",
			"text": {
			"type": "mrkdwn",
			"text": fmt
			}
		}]

		say(blocks=block)
# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

