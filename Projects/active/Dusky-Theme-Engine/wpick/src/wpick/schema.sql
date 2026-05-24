CREATE TABLE IF NOT EXISTS schema_migrations (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS images (
    image_id    TEXT PRIMARY KEY,
    path        TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS features (
    image_id        TEXT PRIMARY KEY,
    oklab_vector    TEXT NOT NULL,
    color_count     INTEGER NOT NULL DEFAULT 0,
    extracted_at    TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clusters (
    cluster_id  INTEGER PRIMARY KEY,
    centroid    TEXT NOT NULL,
    label       TEXT NOT NULL,
    member_count INTEGER NOT NULL DEFAULT 0,
    run_id      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS image_cluster (
    image_id    TEXT NOT NULL,
    cluster_id  INTEGER NOT NULL,
    PRIMARY KEY (image_id),
    FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE,
    FOREIGN KEY (cluster_id) REFERENCES clusters(cluster_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id    TEXT NOT NULL,
    set_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cluster_runs (
    run_id        TEXT PRIMARY KEY,
    ran_at        TEXT NOT NULL DEFAULT (datetime('now')),
    image_count   INTEGER NOT NULL,
    cluster_count INTEGER NOT NULL,
    params        TEXT NOT NULL
);
