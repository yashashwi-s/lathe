L'extension  tablor.sty permet  de créer  des tableaux  de signes  et de
variations depuis latex  en utilisant XCAS pour les  calculs et MetaPOST
pour les tableaux.

On rentre par exemple:

\begin{TV} TV([-10,+infinity],[-1,1],"g","t",x^2/(x^2-1),1,n,\tv) \end{TV} 

et on obtient le tableau de variation de x->x^2/(x^2-1). 

Les tableaux sont construits  à partir du fichier tableauVariation.mp de
Frédéric Mazoit disponible à l'adresse 

http://frederic.mazoit.free.fr/LaTeX_metapost/tableauVariations/

XCAS est téléchargeable à l'adresse :

http://www-fourier.ujf-grenoble.fr/%7Eparisse/giac_fr.html


Les appels à giac ont été améliorés grâce à Yves Delhaye :

http://www.yvesdelhaye.be/?Generateur-d-interrogations-le


Il faut activer le shell-escape.


