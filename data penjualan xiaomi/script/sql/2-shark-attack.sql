WITH brandcomparasion AS (
	SELECT
		"Tanggal",
		"Wilayah",
		max(CASE WHEN "Seri" = 'Black Shark' THEN "Penjualan Harian (Unit)" ELSE 0 end) bs_units,
		max(CASE WHEN "Seri" = 'Xiaomi Flagship' THEN "Penjualan Harian (Unit)" ELSE 0 end) flagship_units
	FROM operational."full" f 
	GROUP BY 1,2
),

growthanalysis AS (
	SELECT 
		*,
		bs_units - lag(bs_units) over(PARTITION BY "Wilayah" ORDER BY "Tanggal") AS bs_growth,
		flagship_units - lag(flagship_units) over(PARTITION BY "Wilayah" ORDER BY "Tanggal") AS flagship_growth
	FROM brandcomparasion
)

SELECT 
	*,
	CASE 
		WHEN bs_growth > 0 AND flagship_growth < 0 THEN 'Potensi Kanibalisasi Tinggi'
		WHEN bs_growth > 0 AND flagship_growth > 0 THEN 'Pasar Tumbuh Bersama'
		ELSE 'Normal/Stabil'
	END AS status_kanibalisasi
FROM growthanalysis
WHERE bs_growth IS NOT NULL ;
	