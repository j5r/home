echo "Para funcionar a compilação, vocẽ deve entrar com um arquivo nanika.pdftex"
echo "Pode ser necessário renomeá-lo para [myfile.pdftex] ou então editar este script"
echo ""

lilypond-book --output=out -f latex --pdf myfile.pdftex
cd out/
pdflatex myfile.tex
mv myfile.pdf ../myfile.pdf
cd ..
rm -rf out



