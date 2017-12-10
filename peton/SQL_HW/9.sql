SELECT l1.Year, l2.Year, Country.Name, (l2.Rate - l1.Rate)/(l2.Year - l1.Year) AS Increase FROM Country
JOIN LiteracyRate AS l1 ON Country.Code = l1.CountryCode
JOIN LiteracyRate AS l2 ON Country.Code = l2.CountryCode AND l2.Year > l1.Year
JOIN LiteracyRate AS lmin ON Country.Code = lmin.CountryCode AND lmin.Year > l1.Year
GROUP BY Country.Code, l1.Year, l2.Year HAVING l2.Year = MIN(lmin.Year)
ORDER BY Increase

