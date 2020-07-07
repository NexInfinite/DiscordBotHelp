# Pycharm Templates
These are some templates that take advantage of pycharm's template variables. 

# Tutorial
1. When you have pycharm open, go to:
<br>
``File > Settings > Editor > File and Code templates``  (Ctrl + Alt + S is a shortcut for settings)
2. Click the + icon 
3. Name it and change the extension to ``py``
4. Copy and paste a template above into the text box below
5. Press ``Apply`` then ``Ok``
6. When you want to use the template do:
    1. ``File > New > The name of the template``
    2. Fill out the form, you can leave items blank
    3. Press ok
    
# Tips
You can find a list of all the variables [here](https://www.jetbrains.com/help/pycharm/file-template-variables.html#predefined_template_variables).
Here are some of the most useful:
<table>
    <tr>
        <th>
            Variable
        </th>
        <th>
            Description
        </th>
    </tr>
    <tr>
        <td>
            ${FILE_NAME}
        </td>
        <td>
            Name of the file - Including file extension
        </td>
    </tr>
    <tr>
        <td>
            ${NAME}
        </td>
        <td>
            Name of the new entity (file, class, interface, and so on)
        </td>
    </tr>
    <tr>
        <td>
            $NameOfVariable
        </td>
        <td>
            Custom variables
        </td>
    </tr>
    <tr>
        <td>
            ${DS}
        </td>
        <td>
            Dollar sign $. This variable is used to escape the dollar character, so that it is not treated as a prefix of a template variable.
        </td>
    </tr>
    <tr>
        <td>
            ${DATE}
        </td>
        <td>
            	
Current system date
        </td>
    </tr>
</table>
