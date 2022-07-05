# Determining exaptations in the use of smartphone applications by using Natural Language Processing
<p>This prototype, which was developed after Design Science as part of my bachelor's thesis, represents an initial attempt to automatically and systematically determine  exaptations in the use of smartphone applications.</p>
<p>Different aspects were used. In the first step, a taxonomy or classification/structuring of apps was necessary (here: IAB Taxonomy). In order to semantically fill this taxonomy, app descriptions were obtained with the help of an app scraper, which were then processed using Natural Language Processing methods in order to be able to assign them as keywords for the respective categories.</p>
<p>Due to the enormous amount of text, it has been saved in a file (dict.json), as otherwise re-referencing this amount would take a lot of time. This text base was saved in a JSON file. This enables the direct use of the program.
Furthermore, individually collected user descriptions of various smartphone apps are evaluated and also assigned to a category in the present taxonomy. This is the part where the insights are established in the eventual exaptative use.</p>
<p>The next step is to determine if there is a match from the category assigned to the smartphone app and the category assigned to the user description. If so, it can be assumed that there is no misuse. Otherwise, the distance between the identified categories is measured (the taxonomy is stored as a non-binary tree). If different main categories are present, an exaptation is assumed.</p>

[Intended Aim of Measuring Exaptations](https://github.com/DoNe158/Exaptations-with-Natural-Language-Processing/files/9045706/description.NLP.pdf)

[Process of determination of exaptations](https://user-images.githubusercontent.com/100798019/177308758-b907105b-23ac-4d33-a8f5-6ca1e549b06e.png)
