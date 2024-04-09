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

# Part 1: Cloning the Repository and preparing VSCode

1. **Locate the Fork Button**: On the top right corner of the repository (this page), you'll see a button labeled "Fork." It's next to the "Watch" and "Star" buttons.

2. **Click Fork**: Click on the "Fork" button. This action will create a copy of the repository under your GitHub account.

3. **Choose the Destination**: A dialog will appear asking where you want to fork the repository. Choose your user account or any organization you're a member of where you want to fork the repository.

4. **Wait for the Fork to Complete**: GitHub will start the process of forking the repository. Depending on the size of the repository, this process may take a few moments.

5. **Confirm Fork Creation**: Once the forking process is complete, you'll be redirected to the forked repository under your GitHub account. You should see a message indicating that the fork was successful.

6. **Clone Your Fork**: In order to work on the forked repository locally, you should clone it to your local machine using Git. Click on the green "Code" button and copy the repository URL. 

7. Open VS Code, go to **'View'**, then **'Command Palette'**, and type **'Git: Clone'**

8. Enter the repository URL you copied: `https://github.com/sergeypechenkin/SpeakItRight-bot`, click 'Clone From URL'

9. Choose a folder on your computer to use as the local Git repository

10. Click '**Open the folder in VS Code**'

That's it! You've successfully forked the repository and can now start making changes to it. Remember, the forked repository is independent of the original repository, so you can make changes without affecting the original project. If you want to contribute your changes back to the original repository, you can do so by creating a pull request.

### Install VSCode extensions:
- Python
- Azure Function

Visual Studio Code (VS Code) extensions are like add-ons or plugins that enhance the functionality of the VS Code editor. They allow you to customize and tailor your coding experience to better suit your needs. 

### Rename example-local.settings.json to local.settings.json
File `local.settings.json` will not be uploaded to the Github repository to prevent a leakage of your secrets

### Create virtual environment:
1. Go to **'View'**, then **'Command Palette'**, and type **'Python: Create environment'**
2. Choose '**Venv**' -> select '**Python x.xx**'
3. Check box on `requirements.txt` to install dependencies, click **'Ok'**

That's it! You've successfully created and activated a virtual environment for your Python project. You can now work on your project within the isolated environment without affecting your system-wide Python installation.
You can activate this environment by opening a project's folder in VSCode and running `.venv\Scripts\activate` script

# Part 2: Creating Azure resources

| Azure Resource type      | Name (example)        | Comments                                                                                                                  |
|--------------------|------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Resource group     | OpenAIBot1-PRD-EUN-rg |  Set the region nearest to you for all resources, except those from OpenAI        |
| Storage account    | openaibot1sa001dsfwd   | storage account names must be between 3 and 24 characters in length and may contain numbers and lowercase letters only. Your storage account name must be unique within Azure                                                                                                                          |
|                    |                        |Go to Storage Account created, Security & Network -> Access Keys -> Show and Copy Connection string. Put it in the local.settings.json
| SA blob container  | history                |                  |
| Function           | OpenAIBot1-PRD-NEU-func     | Settings - Python, 3.11, NEU , Serverless = eventrdiven.  |
| Azure OpenAI       | Openaibot-prd-cae-openai | Check email from csgate@microsoft.com for the Region (We are pleased to inform you that you have been onboarded to Azure OpenAI Service GPT-4 in the CanadaEast region.) <BR>
|||Go to Keys and Deployments and copy Key1 and Endpoint to your local.settings.json. <BR>
|||If you don't have access -  submit this form to request access to OpenAI. [Request Access to OpenAI Service](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUNTZBNzRKNlVQSFhZMU9aV09EVzYxWFdORCQlQCN0PWcu). Corporate subscription and email only. It may take a few days to complete <br>  |
| Open AI Model      | gpt-4     | Go to Azure OpenAI you created, Model Deployments and click Manage Deployments. Click Create new deployment. <br> Model - gpt-4 1106-Preview, Standard, name gpt-4 (hardcoded in the app) |

# Part 3: Deploying your application into Azure Function


1. Go to **'View'**, then **'Command Palette'**, and type '**Azure Functions: Deploy to Azure Function App**'. Sign-in to your Azure account (if not done yet). Choose your '**Subscription**', then choose you '**Function**'. Click `Deploy`. This will overwrite previous application version, if any.  

2. Now we need to get a URL of the application we deployed. 
Go to **'View'**, then **'Command Palette'**, and type '**Azure Functions: Copy Function URL**'. Again, choose your '**Subscription**', '**Function**' and application itself `http_trigger` by default. Paste the URL in the notepad, we will need it later. 

# Part 3: Telegram

1. Find the contact `Botfather` with the blue checkmark
2. Type `/newbot`. Type a **name** for the bot. Your display name that others see in chats and channels. It can be anything you like and changed anytime.
3. Type a **username** for the bot. Unique identifier starting with "@" used for your bot's profile's URL. It helps others find and mention it easily. Once set, it can't be changed or reused. It should end with the `'bot'` word.
4. Copy HTTP API access token and paste the it to your `local.settings.json` file *and* to a notepad temporary

5. Now, it's time to set a webhook to point to our Azure Function app. We will use the Telegram Bot API for that. <br>
The first command we need is: `https://api.telegram.org/bot<token>/setWebhook?url={function_url}` <br>
where `<token>` is your telegram API token, and `{function_url}` is your Function URL. <br> Let's take `https://func1-tg-partybot-3111hb.azurewebsites.net/api/http_trigger` as an example for URL and `6255927130:AAFn8efklsgvy35TYk5MqWwFULknbanF3Js` as a token and construct our example request: <br>

`https://api.telegram.org/bot6255927130:AAFn8efklsgvy35TYk5MqWwFULknbanF3Js/setWebhook?url=https://func1-tg-partybot-3111hb.azurewebsites.net/api/http_trigger` <br><br>
6. Now, copy, paste and run this request in your browser. If constucted correctly, you should see  `"description": "Webhook was set"`.<br>
7. You can check the webhook setting by calling another request: <br>
`https://api.telegram.org/bot<token>/getWebhookInfo`

# Part 4: VS Code - uploading app settings to Azure Function

This marks the final stage of our workshop. 
Our application has been successfully deployed. Now, it's time to configure all the settings we've defined in the `local.settings.json` file.

1. Make sure you have set correctly all settings in your `local.settings.json`.
2. Go to **'View'**, then **'Command Palette'**, and type **'Azure functions: Upload local settings'**. Select your '**Subscription**' and '**Function**'<br><br>

# Congratulations! 🎉 Your bot is now up and running, ready to serve its purpose! Now, it's time to put it to the test.

1. **Open Telegram**: Launch the Telegram app on your device.

2. **Find Your Bot**: In the search bar, type `@mybotuniquename` (replace `mybotuniquename` with your bot's actual username).

3. **Start Chatting**: Once you've found your bot, start a chat with it by clicking on its name. You can now interact with your bot just like you would with any other contact on Telegram!

4. **Test Your Bot**: Try out the commands or actions you've programmed your bot to handle. Whether it's answering questions, providing information, or executing tasks, see how your bot performs in action.

5. **Customize and Iterate**: As you test your bot, take note of any improvements or additional features you'd like to add. Remember, building a bot is an iterative process, so don't hesitate to refine and enhance it based on user feedback and your own observations.

That's it! You've successfully created and deployed your own Telegram bot. I hope you enjoy using it and find it useful for your needs. Happy botting! 🤖✨

