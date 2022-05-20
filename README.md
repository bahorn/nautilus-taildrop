# nautilus-taildrop

Nautilus extension that integrates with
[taildrop](https://tailscale.com/kb/1106/taildrop/).

Essentially, adds a context menu item to nautilus so you can send / receive
files.

As everyone loves a demo, there is one
[here.](https://www.youtube.com/watch?v=KXvxQX_CKx4)

## Install

What I do on my Ubuntu box, might vary between distribution:

```
sudo apt update
sudo apt install python3-nautilus
mdkir -p ~/.local/share/nautilus-python/extensions/
cp taildrop.py ~/.local/share/nautilus-python/extensions/
```

Now just restart nautilus and it should be there when you right click a file.

Make sure your normal user can access the queue with:
```
tailscale up --operator $USER
```

## License

MIT
