package http

import (
	"embed"
	_ "embed"
	"fmt"
	"github.com/drbenton/gin-scoring/internal/domain/queries"
	"html/template"
	"io/fs"
	"net/http"
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

	for _, tmpl := range tmplFiles {
		if tmpl.IsDir() {
			continue
		}

		pt, err := template.ParseFS(files, templatesDir+"/"+tmpl.Name(), layoutsDir+extension)
		if err != nil {
			return err
		}

		templates[tmpl.Name()] = pt
	}
	return nil
}

func HomepageHandler(w http.ResponseWriter, r *http.Request) {
	t, ok := templates["homepage.gohtml"]
	if !ok {
		w.WriteHeader(500)
		fmt.Fprint(w, "Could not load template")
		return
	}

	ctx := r.Context()

	lastGames, err := queries.GetLastGames(ctx)
	if err != nil {
		w.WriteHeader(500)
		fmt.Fprint(w, err.Error())
		return
	}

	hallOfFameGlobal, err := queries.GetHallOfFameGlobal(ctx)
	if err != nil {
		w.WriteHeader(500)
		fmt.Fprint(w, err.Error())
		return
	}

	templateData := make(map[string]interface{})
	templateData["LastGames"] = lastGames
	templateData["hallOfFameGlobal"] = hallOfFameGlobal

	if err := t.Execute(w, templateData); err != nil {
		fmt.Fprintf(w, "Error while rendering template: %#v", err)
		return
	}
}

func PostGameResultHandler(w http.ResponseWriter, r *http.Request) {

}

func PingHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}

func templateFuncs() map[string]interface{} {
	return map[string]interface{}{}
}
