-- Migration: add embeddings table for vector search in MariaDB 11.7.1+
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS embeddings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    source_table VARCHAR(100) NOT NULL,
    source_id BIGINT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    `vector` VECTOR(384) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_source (source_table, source_id),
    KEY idx_source_table (source_table),
    VECTOR INDEX (`vector`) M=8 DISTANCE=cosine
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;