package http

import (
	"embed"
	_ "embed"
	"fmt"
	"github.com/drbenton/gin-scoring/internal/domain/queries"
	"html/template"
	"io/fs"
	"net/http"
	"strings"
)

////go:embed templates/_layout.gohtml
//var layoutHtmlTemplate string
//
////go:embed templates/homepage.gohtml
//var homepageHtmlTemplate string
//
//var layoutTemplate = template.Must(template.New("layout").Funcs(templateFuncs()).Parse(layoutHtmlTemplate))
//var homepageTemplate = template.Must(template.New("homepage").Funcs(templateFuncs()).Parse(homepageHtmlTemplate))
const (
	layoutsDir   = "templates/layouts"
	templatesDir = "templates"
	extension    = "/*.gohtml"
)

var (
	//go:embed templates/*
	files     embed.FS
	templates map[string]*template.Template
)

func LoadTemplates() error {
	// @link https://charly3pins.dev/blog/learn-how-to-use-the-embed-package-in-go-by-building-a-web-page-easily/

	if templates == nil {
		templates = make(map[string]*template.Template)
	}
	tmplFiles, err := fs.ReadDir(files, templatesDir)
	if err != nil {
		return err
	}

	tmplFuncs := templateFuncs()
	for _, tmpl := range tmplFiles {
		if tmpl.IsDir() {
			continue
		}

		fileName := tmpl.Name()
		pt, err := template.New(fileName).Funcs(tmplFuncs).ParseFS(files, templatesDir+"/"+fileName, layoutsDir+extension)
		if err != nil {
			return err
		}

		templates[fileName] = pt
	}
	return nil
}

func HomepageHandler(w http.ResponseWriter, r *http.Request) {
	t, ok := templates["homepage.gohtml"]
	if !ok {
		http.Error(w, "Could not load template", 500)
		return
	}

	ctx := r.Context()

	lastGames, err := queries.GetLastGames(ctx)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	hallOfFameGlobal, err := queries.CalculateHallOfFameGlobal(ctx)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	hallOfFameMonthly, err := queries.CalculateHallOfFameMonthly(ctx)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	templateData := make(map[string]interface{})
	templateData["LastGames"] = lastGames
	templateData["HallOfFameGlobal"] = hallOfFameGlobal
	templateData["HallOfFameMonthly"] = hallOfFameMonthly

	if err := t.Execute(w, templateData); err != nil {
		http.Error(w, fmt.Sprintf("Error while rendering template: %v", err), 500)
		return
	}
}

func PostGameResultHandler(w http.ResponseWriter, r *http.Request) {

}

func PingHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}

func templateFuncs() map[string]interface{} {
	return map[string]interface{}{
		"title": strings.Title,
	}
}
