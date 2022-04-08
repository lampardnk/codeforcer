<div id="header" align="center">
  <img src="https://bit.ly/cf-logo-dis" width="100"/>
</div>

<div id="badges" align="center">
  <a href="https://discord.gg/AThCD7EV">
    <img src="https://img.shields.io/badge/Discord-blue?style=for-the-badge&logo=discord&logoColor=white" alt="LinkedIn Badge"/>
  </a>
  <a href="mailto:nguyenkhackhanhlam@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-red?style=for-the-badge&logo=gmail&logoColor=white" alt="Youtube Badge"/>
  </a>
</div>

<div id="counters" align="center">
  <img src="https://komarev.com/ghpvc/?username=lampardnk&style=flat-square&color=blue" alt=""/>
</div>

# codeforcer
Discord bot for reminding, managing and registering for Codeforces contests
Invite url: https://bit.ly/codeforcer

---

### What is this?
A simple Discord bot with 5 slash-commands (and 1 prefix, for reasons):

- $login {handle} {password}: DM the bot with this command to login to codeforces. This command is needed for /background solves_updater and /contest signup to work properly. Can only link 1 Codeforces handle to 1 Discord username. I'm working on a change linked handle command but I will be keeping the 1:1.  

![image](https://user-images.githubusercontent.com/28803484/162221947-f5f55b32-42d0-421e-90b3-8436377b2c62.png)

---

- /contest list : Return an embed with a list of upcoming Codeforces contests

![image](https://user-images.githubusercontent.com/28803484/162218062-3f7e3a97-9180-4e46-b3d9-a31b5706cefe.png)

---

- /contest summary {contest_id} : Return a summary of the channel members results in a contest

![image](https://user-images.githubusercontent.com/28803484/162221232-7e51d143-88c2-4c09-8385-b90c0f52ceda.png)

---

- /contest signup {handle} : Sign up for ALL Codeforces contests (that are open for register) on codeforces.com itself, using the handle that you logged in with

![image](https://user-images.githubusercontent.com/28803484/162227382-ec11603a-c2dd-41ee-8ede-8f1eb5bf236f.png)

---

- /background check_contest : Can be toggled. Check Codeforces API for all upcoming contests and create discord events for them

![image](https://user-images.githubusercontent.com/28803484/162219000-9320e9da-984d-4352-ad12-83fd4b577a41.png)

![image](https://user-images.githubusercontent.com/28803484/162219083-678da69c-eef4-4712-8b8f-c87ac09386ce.png)

---

- /background solves_updater (y/n) : Can be toggled. Sends a message to the channel the command was used in whenever command user solved a problem 

![image](https://user-images.githubusercontent.com/28803484/162220750-3c217706-815f-44b5-810f-f2008389d8f4.png)

---

### How can I use this?
Invite codeforcer to a server that you have admin rights using this url: https://bit.ly/codeforcer

--- 

### Are my credentials safe?
TLDR: No, I can see them, but no one else can. 

Codeforces credentials sent when you DM the bot with $login will be stored in plaintext in a password-protected MySQL server on AWS RDS. Since codeforcer cogs and other slash commands like /contests signup are used in channels so to cut the need to provide your Codeforces password, it will be stored in plaintext.

I will do my best to ensure that the MySQL server is protected and will absolutely not mess with anyone's credentials in the database.  

---

### You cool how I talk? 
Can contact me through Discord: 0xlampardNK#2683

---

### Last but not least, credits

To people whose code I shamefully copied (but of course, also studied):
- deepak7514: Thank you Sir for your help with /contest signup, I referenced (95%) of your https://github.com/deepak7514/codeforces_automated_registration repository and it is amazing.
- samuzora: Thank you for your sharing with me https://github.com/samuzora/CTF-cord, your bot was my inspiration and your repo structure helped me make mine. Pls check out his CTF Discord bot it is really cool.

:sparkling_heart: Special thanks:

To Lucas (aka samuzora): You are a really cool guy and so is your bot, please keep adding stuff (lol actually fix it first you might not want to add more stuff) to your CTF bot so I can be inspired to add more to mine. Thanks a lot for your help!

And to nkt: Sir thank you for providing me with food and shelter and all kinds of support, both with CP and App Dev, for teaching me whatever I want and need. I would have never even been here without your help or existence. Thank you so much brother!  
