# Welcome to the Azure OpenAI-Powered Telegram Bot Workshop Guide! 🤖✨

Hello and welcome, bot enthusiasts and developers alike!

This comprehensive guide serves as your roadmap to creating your very own Azure OpenAI-powered bot. Whether you're a seasoned developer or just diving into the world of AI, this workshop guide is designed to provide you with detailed instructions and resources every step of the way.

Inside this guide, you'll find:

- Step-by-step instructions for setting up your Azure environment
- Guidance on creating and configuring the necessary Azure resources, including storage accounts, functions, and more
- Tips and best practices for integrating Azure OpenAI into your bot application
- Troubleshooting advice and common pitfalls to avoid

Whether you're looking to build a chatbot, virtual assistant, or something entirely unique, this guide has you covered. Get ready to unleash the power of Azure OpenAI and take your bot-building skills to the next level!

Let's embark on this exciting journey together. Happy coding! 🚀




# Part 1: VS Code

### Install VS Code extensions:
- Python
- Azure Function


### Clone repository:
1. Go to **'View'**, then **'Command Palette'**, and type **'Git: Clone'**
3. Enter the repository URL: `https://github.com/sergeypechenkin/SpeakItRight-bot`, click 'Clone From URL'
4. Choose a folder on your computer to use as the local Git repository
5. Go to **'File'**, select **'Open Folder'**, and then open the created folder

### Create virtual environment:
1. Go to **'View'**, then **'Command Palette'**, and type **'Python: Create environment'**
3. Choose Venv
4. Python
5. Install dependencies

### Rename example-local.settings.json to local.settings.json
File `local.settings.json` will not be uploaded to the Github repository to prevent secret leak

# Part 2: Azure portal

| Azure Resource type      | Name (example)        | Comments                                                                                                                  |
|--------------------|------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Resource group     | OpenAIBot1-PRD-EUN-rg |  Set the region nearest to you for all resources, except those from OpenAI        |
| Storage account    | openaibot1sa001dsfwd   | storage account names must be between 3 and 24 characters in length and may contain numbers and lowercase letters only. Your storage account name must be unique within Azure                                                                                                                          |
|                    |                        |Go to Storage Account created, Security & Network -> Access Keys -> Show and Copy Connection string. Put it in the local.settings.json
| SA blob container  | history                |                  |
| Function           | OpenAIBot1-932u4fh     | Settings - Python, 3.11, NEU , Serverless = eventrdiven.  |
|                    |                        | Open the Function created, Overview, Functions (on the right), click on its Name (http_trigger by default), click "Get Function Url" on the top, copy that and paste to notepad
| Azure OpenAI       | Openaibot-prd-cae-openai | Check email from csgate@microsoft.com for the Region (We are pleased to inform you that you have been onboarded to Azure OpenAI Service GPT-4 in the CanadaEast region.) <br> Go to Keys and Deployments and copy Key1 and Endpoint to your local.settings.json |
| Open AI Model      | gpt-4     | Go to Azure OpenAI you created, Model Deployments and click Manage Deployments. Click Create new deployment. <br> Model - gpt-4 1106-Preview, Standard, name gpt-4 (hardcoded in the app) |

# Part 3: Telegram

1. Find the contact `Botfather` with the blue checkmark
2. Type `/newbot`. Type a **name** for the bot. Can be changed in the future. 
3. Type a **username** for the bot. It should end with the `'bot'` word and cannot be changed in the future.
4. Copy HTTP API access token and paste the it to your `local.settings.json` file and to a notepad temporary

5. Now its time to set a WebHook to point to our Azure Function. We will use Telegram Bot Api for that. <br>
The first command we need is: `https://api.telegram.org/bot<token>/setWebhook?url={function_url}` <br>
where `<token>` is your telegram API token from step 3.4, and `{function_url}` is your Function URL copied in Azure setup part. <br> Let's take `https://func1-tg-partybot-3111hb.azurewebsites.net/api/http_trigger?` as an example for URL and `6255927130:AAFn8efklsgvy35TYk5MqWwFULknbanF3Js` as a token and construct our example request: <br>

`https://api.telegram.org/bot6255927130:AAFn8efklsgvy35TYk5MqWwFULknbanF3Js/setWebhook?url=https://func1-tg-partybot-3111hb.azurewebsites.net/api/http_trigger?` <br><br>
6. Now, copy, paste and run this request in your browser. If constucted correctly, you should see  `"description": "Webhook was set"`
7. You can check the webhook setting by calling another request: <br>
`https://api.telegram.org/bot<token>/getWebhookInfo`

# Part 4: VS Code

This is the last part of the workshop. Now we need to deploy out application to a Function and set variables for it

1. Make sure you have set correctly all settings in your `local.settings.json`.
2. Go to 'View', then 'Command Palette', and type `Azure Function: Deploy to Azure Function App`. Choose your Subscription, then choose you Function created in the 2nd part. Click `Deploy`. This will overwrite previous application version, if any.  