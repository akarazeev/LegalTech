# LegalEngine - qqmbr team

## Inspiration
Our solution makes the client-attorney interaction easier with the use of chat-bot and email notifications, the attorney's work and billing more transparent to the client and easier to follow for the client with the use of visualisation and progress bars.

Since the C&S has two branch offices in Russia - in Moscow and Saint-Petersburg - and Telegram chat-bot is best known messenger platform in Russia - we decided to use this platform as our solution.

## What It does
It's a system that allows to keep a customer up to date on the current status and the progress of the case.

It's easier for client to approve steps, tasks and documents requiring client's approval. This is done with **email notifications** that help the customer to approve some requests by lawyer with simple buttons "Yes"/"I have a comment" and with Telegram **chat-bot**.

The benefits of the Telegram **chat-bot** are that it's more secure than usual email communication, it allows the client to get more detailed information about the case, it allows documents to be attached and reviewed by the client.

**Machine learning** algorithms help the attorney to estimate the case completion **time** and approximate **cost** and through **chat-bot** interface show such information to the client in real-time.

<img src=images/1.jpg width=50%>

| <img src=images/2.jpg>    |  <img src=images/3.jpg>    |
| :------------- | :------------- |
|  <img src=images/6.jpg>      |   <img src=images/4.jpg>     |
| <img src=images/7.jpg>  |  <img src=images/5.jpg>  |

## How we built it
We used Telegram Python API to build a chat-bot. Also we made an email notification system from scratch and also used machine learning library CatBoost to predict the average price of the case and estimated the time for the completion of the case.

## Challenges we ran into
Time. Small amount of data. Building of notification system was pretty challenging task.

## Accomplishments we are proud of
- application of **Machine learning** algorithms in the legal field
- **email** notification system with user's feedback made easy for the user
- introduced **chat-bot** to improve user experience in communication with attorney

## What we learned
That legal field still needs more user friendly interfaces/services.

## What's next for LegalEngine
- the introduction of fixed fees
- help the attorney to draft an offer
- the availability of more historical data makes the predictions of total costs and time more reliable

## Try it out
- [GitHub Repo](https://github.com/akarazeev/LegalTech)
- [t.me/legal_tech_bot](https://t.me/legal_tech_bot)
- [Devpost](https://devpost.com/software/legalengine)
