SELECT Country.Name, l1.Rate
FROM Country
JOIN LiteracyRate AS l1 ON Country.Code = l1.CountryCode
JOIN LiteracyRate AS lmax ON Country.Code = lmax.CountryCode
GROUP BY Country.Code, l1.Year 
HAVING l1.Year = MAX(lmax.Year)
ORDER BY l1.Rate DESC
LIMIT 1