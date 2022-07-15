package internal

import "github.com/spf13/viper"

type config struct {
	DatabaseURL string
}

var configSingleton *config

func Config() *config {
	if configSingleton == nil {
		viper.AutomaticEnv()
		viper.SetDefault("DATABASE_URL", "postgres://ginscoringuser:localdev@localhost:5433/ginscoring?sslmode=disable")

		configSingleton = &config{
			DatabaseURL: viper.GetString("DATABASE_URL"),
		}
	}

	return configSingleton
}
