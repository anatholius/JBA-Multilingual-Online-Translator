# Multilingual Online Translator

## Objectives - `Stage 2/7`

At this stage, your program should:

1. Take an input specifying the target language (en if the user wants to
   translate from French into English, or fr if the user wants to translate
   from English into French).
2. Take an input specifying the word that should be translated.
3. Output the confirmation message in the format You chose "..." as a language
   to translate "...".
4. Form a request and connect to ReversoContext.
5. Check the HTTP status of the response of the website to your request. If the
   status code is 200, you are good to proceed! If not... Try again?
6. Output the response of the website to your request (200) and OK message to
   show that the connection is successful (so, the entire line should be 200
   OK).
7. Output the line Translations.
8. Output a list with translations of the given word in the target
   language: ['bonjour', 'salut'].
9. Output a list with examples of sentences featuring the given word or any of
   its translations:
   `['Well, hello, freedom fighters.', 'Et bien, bonjour combattants de la liberté.']`

   Both the original versions of the sentences and their translations should
   be printed. You don't need to filter sentences in any way: just print all
   the sentences that ReversoContext output for the given language pair and the
   given word.

Make sure you output exactly the sentences that ReversoContext shows initially
on the
page https://context.reverso.net/translation/{language_1}-{language_2}/{word}.
Don't confound them with the sentences that the website shows when you click on
the first translation equivalent. These sentences will not be accepted by
tests.
