require("dotenv").config();

const express = require("express");
const mongoose = require("mongoose");

const app = express();
const Song = require("./models/Song");
const Genre = require("./models/Genre");
const Artist = require("./models/Artist");
const Album = require("./models/Album");

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((err) => {
    console.error("Connection error:", err.message);
    process.exit(1);
  });

app.use(express.json());

// songs
app.get("/songs", async (req, res) => {
  try {
    const {
      original_name,
      album_title,
      album_code,
      genre_name,
      artist_name,
      limit = 10,
      offset = 0,
    } = req.query;

    let filter = {};

    if (original_name) {
      filter.original_name = { $regex: new RegExp(original_name, "i") };
    }

    if (album_title || album_code) {
      const albumFilter = {};
      if (album_title)
        albumFilter.title = { $regex: new RegExp(album_title, "i") };
      if (album_code) albumFilter.code = album_code;

      const albums = await Album.find(albumFilter).select("_id");
      filter.album = { $in: albums.map((album) => album._id) };
    }

    if (genre_name) {
      const genres = await Genre.find({
        name: { $regex: new RegExp(genre_name, "i") },
      }).select("_id");
      filter.genre = { $in: genres.map((genre) => genre._id) };
    }

    if (artist_name) {
      const artists = await Artist.find({
        name: { $regex: new RegExp(artist_name, "i") },
      }).select("_id");
      filter.artists = { $in: artists.map((artist) => artist._id) };
    }

    console.log(limit);

    const songs = await Song.find(filter)
      .populate("album", "code title year thumbnail300x300 thumbnail")
      .populate("genre", "name")
      .populate("artists", "name artists_thumbnail300x300 artists_thumbnail")
      .skip(parseInt(offset))
      .limit(parseInt(limit));

    res.json(songs);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get("/song/:id", async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ message: "Invalid ID format" });
    }

    const song = await Song.findById(id)
      .populate("album", "code title year thumbnail300x300 thumbnail")
      .populate("genre", "name")
      .populate("artists", "name artists_thumbnail300x300 artists_thumbnail");

    if (!song) {
      return res.status(404).json({ message: "Song not found" });
    }

    res.json(song);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// artists
app.get("/artists", async (req, res) => {
  try {
    const { name, limit = 10, offset = 0 } = req.query;

    const pipeline = [];

    const matchStage = {};

    if (name) {
      matchStage.name = { $regex: new RegExp(name, "i") };
    }

    if (Object.keys(matchStage).length > 0) {
      pipeline.push({ $match: matchStage });
    }

    pipeline.push({ $skip: parseInt(offset) }, { $limit: parseInt(limit) });

    const artists = await Artist.aggregate(pipeline);

    res.json(artists);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get("/artist/:id", async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ message: "Invalid ID format" });
    }

    const artist = await Artist.findById(id);

    if (!artist) {
      return res.status(404).json({ message: "Artist not found" });
    }

    res.json(artist);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// albums
app.get("/albums", async (req, res) => {
  try {
    const { code, title, year, limit = 10, offset = 0 } = req.query;

    const pipeline = [];

    const matchStage = {};

    if (code) {
      matchStage.code = { $regex: new RegExp(code, "i") };
    }

    if (title) {
      matchStage.title = { $regex: new RegExp(title, "i") };
    }

    if (year) {
      matchStage.year = parseInt(year);
    }

    if (Object.keys(matchStage).length > 0) {
      pipeline.push({ $match: matchStage });
    }

    pipeline.push({ $skip: parseInt(offset) }, { $limit: parseInt(limit) });

    const albums = await Album.aggregate(pipeline);

    res.json(albums);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get("/album/:id", async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ message: "Invalid ID format" });
    }

    const album = await Album.findById(id);

    if (!album) {
      return res.status(404).json({ message: "Album not found" });
    }

    res.json(album);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// genres
app.get("/genres", async (req, res) => {
  try {
    const { name, limit = 10, offset = 0 } = req.query;

    const pipeline = [];

    const matchStage = {};

    if (name) {
      matchStage.name = { $regex: new RegExp(name, "i") };
    }

    if (Object.keys(matchStage).length > 0) {
      pipeline.push({ $match: matchStage });
    }

    pipeline.push({ $skip: parseInt(offset) }, { $limit: parseInt(limit) });

    const genres = await Genre.aggregate(pipeline);

    res.json(genres);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get("/genre/:id", async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ message: "Invalid ID format" });
    }

    const genre = await Genre.findById(id);

    if (!genre) {
      return res.status(404).json({ message: "Genre not found" });
    }

    res.json(genre);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
