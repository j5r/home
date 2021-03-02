package main

import (
	"fmt"
	"log"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request){
	var texto = "<html><style>img{width:99vw;}</style>\n<img src=\"https://hdqwalls.com/wallpapers/kaneki-ken-tokyo-ghoul-q6.jpg\" alt=\"\"></img><a href=\"https://1.bp.blogspot.com/-egLGJOFCq7Y/Trkm7dmIIAI/AAAAAAAAAGg/nulr2ixOi88/s1600/final_getsuga_tenshou_by_24352345.jpg\">.</a>\n</html>"
	fmt.Fprintf(w, texto)
}

func main(){
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8081", nil))
}