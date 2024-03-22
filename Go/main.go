package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
)

const ROOT_URL string = "https://api.irail.be/liveboard"
const TIME_DELTA int = 15
const DEFAULT_STATION_1 string = "Schaerbeek"
const DEFAULT_STATION_2 string = "Bordet"

func main() {

	resource := "liveboard"
	params := url.Values{}
	params.Add("station", DEFAULT_STATION_1)
	params.Add("format", "json")
	params.Add("lang", "en")
	params.Add("alerts", "true")
	params.Add("time", "1000")

	u, _ := url.ParseRequestURI(ROOT_URL)
	u.Path = resource
	u.RawQuery = params.Encode()
	urlstr := fmt.Sprintf("%v", u)

	// Debug
	fmt.Println(urlstr)

	res, err := http.Get(urlstr)
	if err != nil {
		log.Fatal(err)
	}
	body, err := io.ReadAll(res.Body)
	res.Body.Close()
	if res.StatusCode > 299 {
		log.Fatalf("Response failed with status code: %d and\nbody: %s\n", res.StatusCode, body)
	}
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s", body)

}
