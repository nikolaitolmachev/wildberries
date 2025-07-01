import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Slider,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableSortLabel,
  Box,
  Typography,
} from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
} from "recharts";

function App() {
  // Filter states
  const [priceRange, setPriceRange] = useState([0, 10000]);
  const [minRating, setMinRating] = useState(4.8);
  const [minFeedbacks, setMinFeedbacks] = useState(1000);

  // Sorting states
  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  // Product data
  const [products, setProducts] = useState([]);

  // Loading data from API
  const fetchProducts = async () => {
    try {
      // Forming request parameters
      const params = {
        min_price: priceRange[0],
        max_price: priceRange[1],
        min_rating: minRating,
        min_feedbacks: minFeedbacks,
      };

      const response = await axios.get("/api/products/", { params });
      let data = response.data;

      // Sorting on the client
      if (sortField) {
        data = [...data].sort((a, b) => {
          let valA = a[sortField];
          let valB = b[sortField];

          if (typeof valA === "string") {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
          }

          if (valA < valB) return sortOrder === "asc" ? -1 : 1;
          if (valA > valB) return sortOrder === "asc" ? 1 : -1;
          return 0;
        });
      }

      setProducts(data);
    } catch (error) {
      console.error("Error loading products:", error);
    }
  };

  // Auto-update when filters or sorting changes
  useEffect(() => {
    fetchProducts();
  }, [priceRange, minRating, minFeedbacks, sortField, sortOrder]);

  // Filter change handlers
  const handlePriceChange = (event, newValue) => {
    setPriceRange(newValue);
  };

  const handleMinRatingChange = (event) => {
    setMinRating(Number(event.target.value));
  };

  const handleMinFeedbacksChange = (event) => {
    setMinFeedbacks(Number(event.target.value));
  };

  // Sorting handler
  const handleSort = (field) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  // Data for the price histogram (splitting it into ranges of 1000)
  const histogramData = [];
  const maxPrice = priceRange[1];
  const binSize = 1000;
  for (let i = 0; i <= maxPrice; i += binSize) {
    const count = products.filter(
      (p) =>
        p.price_with_discount >= i && p.price_with_discount < i + binSize
    ).length;
    histogramData.push({
      priceRange: `${i}-${i + binSize - 1}`,
      count,
    });
  }

  // Data for line chart (discount = price_basic - price_with_discount)
  const lineData = products.map((p) => ({
    discount: p.price_basic - p.price_with_discount,
    rating: p.rating,
  }));

  return (
    <Box sx={{ padding: 4, textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom>
        Table of products with filters and graphs
      </Typography>

      {/* Filters */}
      <Box sx={{ display: "flex", gap: 8, marginBottom: 4, marginTop: 6, justifyContent: "center"}}>
        <Box sx={{ width: 300 }}>
          <Typography>Price range</Typography>
          <Slider
            value={priceRange}
            onChange={handlePriceChange}
            valueLabelDisplay="auto"
            min={0}
            max={100000}
            step={500}
          />
        </Box>

        <TextField
          label="Rating >="
          type="number"
          inputProps={{ min: 0, max: 5, step: 0.1 }}
          value={minRating}
          onChange={handleMinRatingChange}
        />

        <TextField
          label="Count of feedbacks >="
          type="number"
          inputProps={{ min: 0, step: 10 }}
          value={minFeedbacks}
          onChange={handleMinFeedbacksChange}
        />
      </Box>

      {/* Product table */}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>
              <TableSortLabel
                active={sortField === "name"}
                direction={sortOrder}
                onClick={() => handleSort("name")}
              >
                Product
              </TableSortLabel>
            </TableCell>
            <TableCell>
              <TableSortLabel
                active={sortField === "price_with_discount"}
                direction={sortOrder}
                onClick={() => handleSort("price_with_discount")}
              >
                Discounted price (₽)
              </TableSortLabel>
            </TableCell>
            <TableCell>Price (₽)</TableCell>
            <TableCell>
              <TableSortLabel
                active={sortField === "rating"}
                direction={sortOrder}
                onClick={() => handleSort("rating")}
              >
                Rating
              </TableSortLabel>
            </TableCell>
            <TableCell>
              <TableSortLabel
                active={sortField === "feedbacks"}
                direction={sortOrder}
                onClick={() => handleSort("feedbacks")}
              >
                Feedbacks
              </TableSortLabel>
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {products.map((p) => (
            <TableRow key={p.id}>
              <TableCell> <a href={`https://www.wildberries.ru/catalog/${p.id_wb}/detail.aspx/`}>{p.name}</a></TableCell>
              <TableCell>{p.price_with_discount}</TableCell>
              <TableCell>{p.price_basic}</TableCell>
              <TableCell>{p.rating}</TableCell>
              <TableCell>{p.feedbacks}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Charts */}
      <Box sx={{ display: "flex", gap: 10, marginTop: 6, justifyContent: "center"}}>
        <Box sx={{ width: 500, height: 300 }}>
          <Typography variant="h6" gutterBottom>
            Price histogram
          </Typography>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={histogramData}>
              <XAxis dataKey="priceRange" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#1976d2" />
            </BarChart>
          </ResponsiveContainer>
        </Box>

        <Box sx={{ width: 500, height: 300 }}>
          <Typography variant="h6" gutterBottom>
            Discount vs Rating
          </Typography>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={lineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="discount" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="rating"
                stroke="#ff7300"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </Box>
    </Box>
  );
}

export default App;
