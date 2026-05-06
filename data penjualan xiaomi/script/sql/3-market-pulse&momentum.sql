SELECT 
	"Tanggal",
	"Asia",
	round((("Asia" - LAG("Asia") OVER (ORDER BY "Tanggal"))::NUMERIC / NULLIF (LAG("Asia") OVER (ORDER BY "Tanggal"), 0)) * 100, 2) AS asia_growth,
	"Europe",
	round((("Europe" - LAG("Europe") OVER (ORDER BY "Tanggal"))::NUMERIC / NULLIF (LAG("Europe") OVER (ORDER BY "Tanggal"), 0)) * 100, 2) AS europe_growth,
	"Latin America",
	"Middle East & Africa"
FROM operational.region r 
ORDER BY "Tanggal" ;