
install:
	mkdir -p ~/.local/share/nautilus-python/extensions/
	cp taildrop.py ~/.local/share/nautilus-python/extensions/

deinstall:
	@rm ~/.local/share/nautilus-python/extensions/taildrop.py | true

