install_dir = ${HOME}/.local/bin/
name = jyou

make:
	cd src/; zip -r ../${name}.zip *
	echo "#!/usr/bin/env python" | cat - ${name}.zip > ${name}

install:
	pip install Pillow tqdm
	install -D -m 700 ${name} ${install_dir}

clean:
	rm -f ${name}{,.zip}
	