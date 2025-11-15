# Q1. Summary

The purpose of this project is to build a collection of chat-bots that use recurrent neural networks (RNN) and transformers acrhictures to act as players in a session of Dungeons and Dragons.

There are three chat bots implemented: Godel - developed by Microsoft as a text to text generation model, Blender bot - developed by meta/Facebook also as a simple text to text generation model, and a RNN - using keras and trained on 1000 entries for the Fireball dataset

The dataset used for this project is Fireball. Approximately 60gb of game state information of Dungeons and Dragons session over discord. player turn descriptions are extracted from this and used as the training data fir text generation.

Four Discord bots were built. The first one acting as a managerial bot for the language models, handling player commands. The other three bots implement the trained language models.

# Q2. Dataset Description

## Dataset Description

This project uses FIREBALL: A Dataset of Dungeons and Dragons Actual-Play with Structured Game State Information. The data set contains nearly 25,000 turns from multiple Dungeons and Dragons campaigns. Data is broken up into two files: raw and filtered. The raw data is the direct output from the Avrae Discord bot, containing player information, what the player said, and other game state items. The filtered data contains information about each entire turn. It is broken into three parts: before utterances – the game state before the turn, events – all the stuff that happens in the turn, and after utterances – the turn results. The content of what each player said is in all three of these sections.

For This project I have further filtered the data to a collection of sentences in sequence i.e. the flow of conversation in the collection of dnd sessions. there are 344634 sentences, 5114768 words, with an average of 15 words per sentence.

## Perplexity Score

It is difficult to calculate the AUC score for textual data and language models as text generation isn't a classification  task. I have provided The perplexity scores of each model for the opening of the dnd session and the bots responses.

Session opening: You are a party of 3 on a trek across through a snowy boreal forest. You have all been traveling for a week now, and the rations are slim. You have set up camp for the night by a river. The 3 of you sit around the crackling fire, trying to stay warm. Suddenly, you hear a noise, some twigs snapping deep in the woods. you are all on high alert. Suddenly 5 goblins appear from the woods all crying rusty swords and axes. what do you do now?

fbRnnAdomModel:  right the same in each form except for the speed changes noted any equipment it
name: fbRnnAdomModel, perplexity: 0.3690816765487051

microsoft/GODEL-v1_1-base-seq2seq: Get a knife. Kill them. Make a fire.
name: microsoft/GODEL-v1_1-base-seq2seq, perplexity: 0.37664428062602673

facebook/blenderbot-400M-distill:  I don't know what we are going to do.  I am so scared of them.
name: facebook/blenderbot-400M-distill, perplexity: 0.3694251849513593


# Q3. Details
The three models were implemented using a similar framework, promarily suing two functions: readInUtterances() and generateResponse(). Godel and Blender Bot are pre-trained models imported from Hugging Face while the RNN (named Raven) was directly train on data from Firefball. These methods are Implemented by the lmDiscordBot.py. dndBotManagerDB.py acts as the main script for the three models. This script contains the discord commands to run the three models. 

For the models the readInUtterance() function reads in the latest message the user has sent. Both Godel and the RNN model can only handle up to five hundred tokens at a time. If this token count is reached, the oldest utterance is removed from the chat history. At any given time, chat history may contain approximately fifty sequential utterances, providing good context for the model to generate a response. Blender Bot can only handle one hundred and twenty eight tokens at a time, which means it can on take in two or three sequential utterances. Blender bot still produced good responses but lost context very quickly. The generateResponse() function works slightly differently for each model. Godel takes in three groups of information: a knowledge  base containing information on what it is to talk about, instructions on who it is and how it should act, and the chat history. Godel also uses a degree of randomness as it generate a different response  each time when given the same prompt. Blender Bot doesn't take in any extra information and only relies on the small amount of information in the chat history. The RNN model takes in the same chat history as Godel, but will only generate up to fifteen new words. Any more then fifteen and it tends to start repeating phrases.

Fireball contains all game state information of a collection of Dungeons and Dragons session. Not all of this information is important so only the utterances were scraped. The before, during, and after utterances were added to the sentances.json file. The RNN was only trained on the first one thousand entries due to processing time.

All models had middling performance. The RNN produced the most "dnd sounding" responses. Although most of the responses were gibberish, a small about of the response was related to the prompt. Blender Bot was the best at playing along with the narrative. most of responses were directly related to the situation happening in the session. Godel seemed to preform the worst and often gave nonsensical response. It would often send its own id tag or one of the other bots tags. It also had a lot of incomplete sentences. Despite all the extra information it was given, it had a hard time keeping context.