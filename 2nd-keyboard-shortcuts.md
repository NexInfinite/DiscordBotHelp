# Double Keyboards

## How to Setup

1. You need to install LuaMacros \([http://www.hidmacros.eu/forum/viewtopic.php?f=10&t=241\#p794](http://www.hidmacros.eu/forum/viewtopic.php?f=10&t=241#p794)\)
2. Download the script above \([2ndKeyboard.lua](https://github.com/NexInfinite/DiscordBotHelp/tree/a3607068536fa4e82d8902c21ed6762dad9ff144/2nd%20Keyboard%20Shortcuts/2ndKeyboard.lua)\)
3. Run LuaMacros
4. Click the top left icon \(blue box with white slip\)
5. Double click the script you just downloaded and hit play.

The basic setup has now been installed!

## Other Information

The code I have provided above uses they keys \, z, x, c, LeftArrow, RightArrow.

*  sends the  key \(My main keyboard doesnt have this button\)
* z sends \n 
* x sends multiple keys that makes an embed.
* c sends the embed add\_field
* LeftArrow presses LeftArrow 15 times \(I use this for video editing\)
* RightArrow presses RightArrow 15 times \(I also use this for video editing\)

To add a new hotkey copy and edit the code below:

```text
if (button == 90) then
    lmc_send_keys("\\n")
    end
```

If you want to not have to press a new key on your keyboard every time you use luamacros, follow the instructions that Taran made.

It is also useful to not that you will need some basic understanding of LuaMacros, its very simple to learn so just read around.

## Please Note

I was not the one who came up with this. I have only edited Taran's code \([https://github.com/TaranVH/2nd-keyboard/tree/master/LUAMACROS](https://github.com/TaranVH/2nd-keyboard/tree/master/LUAMACROS)\).

