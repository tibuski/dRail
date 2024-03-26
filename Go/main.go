package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"net/url"
	"time"
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

type Liveboard struct {
	Version     string `json:"version"`
	Timestamp   string `json:"timestamp"`
	Station     string `json:"station"`
	Stationinfo struct {
		LocationX    string `json:"locationX"`
		LocationY    string `json:"locationY"`
		ID           string `json:"id"`
		Name         string `json:"name"`
		ID0          string `json:"@id"`
		Standardname string `json:"standardname"`
	} `json:"stationinfo"`
	Departures struct {
		Number    string `json:"number"`
		Departure []struct {
			ID          string `json:"id"`
			Delay       string `json:"delay"`
			Station     string `json:"station"`
			Stationinfo struct {
				LocationX    string `json:"locationX"`
				LocationY    string `json:"locationY"`
				ID           string `json:"id"`
				Name         string `json:"name"`
				ID0          string `json:"@id"`
				Standardname string `json:"standardname"`
			} `json:"stationinfo"`
			Time        string `json:"time"`
			Vehicle     string `json:"vehicle"`
			Vehicleinfo struct {
				Name      string `json:"name"`
				Shortname string `json:"shortname"`
				Number    string `json:"number"`
				Type      string `json:"type"`
				LocationX string `json:"locationX"`
				LocationY string `json:"locationY"`
				ID        string `json:"@id"`
			} `json:"vehicleinfo"`
			Platform     string `json:"platform"`
			Platforminfo struct {
				Name   string `json:"name"`
				Normal string `json:"normal"`
			} `json:"platforminfo"`
			Canceled            string `json:"canceled"`
			Left                string `json:"left"`
			IsExtra             string `json:"isExtra"`
			DepartureConnection string `json:"departureConnection"`
		} `json:"departure"`
	} `json:"departures"`
}

func queryLiveboard(station string, timeDelta int) (Liveboard, error) {

	now := time.Now()
	time := now.Add(-time.Minute * time.Duration(timeDelta))

	resource := "liveboard"
	params := url.Values{}
	params.Add("station", station)
	params.Add("format", RESPONSE_FORMAT)
	params.Add("lang", RESPONSE_LANG)
	params.Add("alerts", RESPONSE_ALERT)
	params.Add("time", time.Format("1504"))

	u, _ := url.ParseRequestURI(ROOT_URL)
	u.Path = resource
	u.RawQuery = params.Encode()
	urlstr := fmt.Sprintf("%v", u)

	fmt.Println(urlstr) // Debug

	resp, err := http.Get(urlstr)
	if err != nil {
		log.Fatal(err)
	}

	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	var result Liveboard

	err = json.Unmarshal(body, &result)

	if err != nil {
		fmt.Println("Can not unmarshal JSON")
	}

	return result, err

}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	p, err := queryLiveboard(DEFAULT_STATION_1, TIME_DELTA)
	if err != nil {
		log.Fatal(err)
	}

	t, err := template.ParseFiles("html/liveboard.html")
	if err != nil {
		log.Fatal(err)
	}
	t.Execute(w, p)
}

func main() {

	mux := http.NewServeMux()
	mux.HandleFunc("GET /drail/", rootHandler)

	fs := http.FileServer(http.Dir("html/static"))
	mux.Handle("/static/", http.StripPrefix("/static/", fs))

	fmt.Println("Sarting server on http://localhost:8080/drail")

	err := http.ListenAndServe("localhost:8080", mux)

	if err != nil {
		log.Fatal(err)
	}

}
