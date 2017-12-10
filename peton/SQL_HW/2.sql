SELECT Country.Name, MAX(LiteracyRate.Rate) FROM LiteracyRate
JOIN Country ON Country.Code = LiteracyRate.CountryCode