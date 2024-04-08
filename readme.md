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

# Part 1: Clone repository

1. **Locate the Fork Button**: On the top right corner of the repository (this page), you'll see a button labeled "Fork." It's next to the "Watch" and "Star" buttons.

2. **Click Fork**: Click on the "Fork" button. This action will create a copy of the repository under your GitHub account.

3. **Choose the Destination**: A dialog will appear asking where you want to fork the repository. Choose your user account or any organization you're a member of where you want to fork the repository.

4. **Wait for the Fork to Complete**: GitHub will start the process of forking the repository. Depending on the size of the repository, this process may take a few moments.

5. **Confirm Fork Creation**: Once the forking process is complete, you'll be redirected to the forked repository under your GitHub account. You should see a message indicating that the fork was successful.

6. **Clone Your Fork**: In order to work on the forked repository locally, you should clone it to your local machine using Git. Click on the green "Code" button and copy the repository URL. 

7. Open VS Code, go to **'View'**, then **'Command Palette'**, and type **'Git: Clone'**

8. Enter the repository URL you copied: `https://github.com/sergeypechenkin/SpeakItRight-bot`, click 'Clone From URL'

9. Choose a folder on your computer to use as the local Git repository

10. Go to **'File'**, select **'Open Folder'**, and then open the created folder

That's it! You've successfully forked the repository and can now start making changes to it. Remember, the forked repository is independent of the original repository, so you can make changes without affecting the original project. If you want to contribute your changes back to the original repository, you can do so by creating a pull request.

# Part 2: VS Code

### Install VS Code extensions:
- Python
- Azure Function

Visual Studio Code (VS Code) extensions are like add-ons or plugins that enhance the functionality of the VS Code editor. They allow you to customize and tailor your coding experience to better suit your needs. 

### Create virtual environment:
1. Go to **'View'**, then **'Command Palette'**, and type **'Python: Create environment'**
2. Choose .venv -> Python
3. Install dependencies

That's it! You've successfully created and activated a virtual environment for your Python project. You can now work on your project within the isolated environment without affecting your system-wide Python installation.
You can activate this environment by opening a project's folder in VSCode and running `.venv\Scripts\activate` script

### Rename example-local.settings.json to local.settings.json
File `local.settings.json` will not be uploaded to the Github repository to prevent a leakage of your secrets

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