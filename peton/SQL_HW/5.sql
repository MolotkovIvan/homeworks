SELECT Country.GovernmentForm, SUM(Country.SurfaceArea) AS TotalArea
FROM Country
GROUP BY Country.GovernmentForm
ORDER BY TotalArea DESC
LIMIT 1
