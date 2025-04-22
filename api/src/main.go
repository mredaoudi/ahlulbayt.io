package main

import (
    "embed"
    "encoding/json"
    "log"
    "net/http"
    "strconv"

    "github.com/gin-gonic/gin"
)

//go:embed data/quran.json
var quranFS embed.FS

type Ayah struct {
    AyahNumber        int    `json:"_n"`
    ArabicText        string `json:"ar"`
    EnglishText       string `json:"en"`
}

type Surah struct {
    ArabicName               string `json:"ar"`
    EnglishName              string `json:"en"`
    Number                   int    `json:"_n"`
    Transliteration          string `json:"_a"`
    NumberOfAyahs            int    `json:"_c"`
    Ayahs                    []Ayah `json:"_v"`
    Location                 string `json:"_l"`
}

var surahs []Surah

func loadQuranData() {
    data, err := quranFS.ReadFile("data/quran.json")
    if err != nil {
        log.Fatalf("Failed to read Quran data: %v", err)
    }

    if err := json.Unmarshal(data, &surahs); err != nil {
        log.Fatalf("Failed to unmarshal Quran data: %v", err)
    }

    log.Printf("Loaded %d surahs", len(surahs))
}

func getAllSurahs(c *gin.Context) {
    type SurahSummary struct {
        ArabicName               string `json:"ar"`
        EnglishName              string `json:"en"`
        Number                   int    `json:"_n"`
        Transliteration          string `json:"_a"`
        NumberOfAyahs            int    `json:"_c"`
        Location                 string `json:"_l"`
    }

    summaries := make([]SurahSummary, len(surahs))
    for i, surah := range surahs {
        summaries[i] = SurahSummary{
            ArabicName:      surah.ArabicName,
            EnglishName:     surah.EnglishName,
            Number:          surah.Number,
            Transliteration: surah.Transliteration,
            NumberOfAyahs:   surah.NumberOfAyahs,
            Location:        surah.Location,
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "surahs": summaries,
    })
}

func getSurahByNumber(c *gin.Context) {
    surahNumber, err := strconv.Atoi(c.Param("num"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid surah number"})
        return
    }

    for _, surah := range surahs {
        if surah.Number == surahNumber {
            c.JSON(http.StatusOK, surah)
            return
        }
    }

    c.JSON(http.StatusNotFound, gin.H{
        "error": "Surah not found",
    })
}

func main() {
    loadQuranData()

    r := gin.Default()

    r.GET("/quran", getAllSurahs)
    r.GET("/quran/:num", getSurahByNumber)

    log.Println("Server starting on :8080...")
    if err := r.Run(":8080"); err != nil {
        log.Fatalf("Failed to start server: %v", err)
    }
}