WITH DailyRank AS (
	SELECT 
		"Tanggal",
		"Wilayah",
		"Seri",
		"Penjualan Harian (Unit)",
		row_number() over(PARTITION BY "Tanggal", "Wilayah" ORDER BY "Penjualan Harian (Unit)" DESC) AS rank_dominansi 
	FROM operational."full" f 
)

SELECT 
	"Tanggal",
	"Wilayah" AS wilayah_label, 
	CASE 
		
		WHEN "Wilayah" = 'Asia' THEN 'Asia' 
		WHEN "Wilayah" = 'Europe' THEN 'Europe'
		WHEN "Wilayah" = 'Latin America' THEN 'South America' 
		WHEN "Wilayah" = 'Middle East & Africa' THEN 'Africa' 
		ELSE "Wilayah"
	END AS wilayah_map, 
	"Seri" AS seri_dominan,
	"Penjualan Harian (Unit)" AS volume_penjualan
FROM DailyRank
WHERE rank_dominansi = 1
ORDER BY "Tanggal", "Wilayah";