-- Table des entreprises
CREATE TABLE Companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL
);
CREATE TABLE Country (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL
);
CREATE TABLE salary (
    salary_id INT AUTO_INCREMENT PRIMARY KEY,
    salary INT NOT NULL
);

CREATE TABLE date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    year int,
    month int,
    day int
);

-- Table des types de contrat
CREATE TABLE ContractTypes (
    contract_type_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_type VARCHAR(255) NOT NULL
);

-- Table des niveaux d'expérience
CREATE TABLE ExperienceLevels (
    experience_level_id INT AUTO_INCREMENT PRIMARY KEY,
    experience_level VARCHAR(255) NOT NULL
);

-- Table des emplacements
CREATE TABLE Locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255) NOT NULL
);

-- Table des secteurs
CREATE TABLE Sectors (
    sector_id INT AUTO_INCREMENT PRIMARY KEY,
    sector VARCHAR(255) NOT NULL
);

-- Table des compétences
CREATE TABLE Skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill VARCHAR(255) NOT NULL
);

-- Table des titres
CREATE TABLE Titles (
    title_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

-- Table des contrats (table de faits)
CREATE TABLE Jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    contract_type_id INT,
    experience_level_id INT,
    location_id INT,
    sector_id INT,
    skill_id INT,
    title_id INT,
    salary_id INT,
    date_id int,
    country_id int,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id),
    FOREIGN KEY (contract_type_id) REFERENCES ContractTypes(contract_type_id),
    FOREIGN KEY (experience_level_id) REFERENCES ExperienceLevels(experience_level_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id),
    FOREIGN KEY (sector_id) REFERENCES Sectors(sector_id),
    FOREIGN KEY (skill_id) REFERENCES Skills(skill_id),
    FOREIGN KEY (title_id) REFERENCES Titles(title_id),
    FOREIGN KEY (salary_id) REFERENCES salary(salary_id),
    FOREIGN KEY (date_id) REFERENCES date(date_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

