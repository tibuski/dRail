package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
)

const (
	ROOT_URL          string = "https://api.irail.be/liveboard"
	TIME_DELTA        int    = 15
	DEFAULT_STATION_1 string = "Schaerbeek"
	DEFAULT_STATION_2 string = "Bordet"
	RESPONSE_FORMAT   string = "json"
	RESPONSE_LANG     string = "en"
	RESPONSE_ALERT    string = "true"
)

func queryLiveboard(station string, time string) ([]byte, error) {

	resource := "liveboard"
	params := url.Values{}
	params.Add("station", station)
	params.Add("format", RESPONSE_FORMAT)
	params.Add("lang", RESPONSE_LANG)
	params.Add("alerts", RESPONSE_ALERT)
	params.Add("time", time)

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

	return body, err

}

func main() {

	resp, err := queryLiveboard("Soignies", "1600")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Print("%v", []byte(resp))

}
