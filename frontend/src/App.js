import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Box,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [tab, setTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [models, setModels] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [customerData, setCustomerData] = useState({
    customer_id: 'CUST_00001',
    age: 45,
    tenure: 12,
    monthly_charges: 70.5,
    total_charges: 846.0,
    contract_type: 'Month-to-month',
    payment_method: 'Electronic check',
    paperless_billing: true,
    gender: 'Male',
    partner: false,
    dependents: false,
    phone_service: true,
    multiple_lines: false,
    internet_service: 'Fiber optic',
    online_security: false,
    online_backup: false,
    device_protection: false,
    tech_support: false,
    streaming_tv: true,
    streaming_movies: true,
  });

  useEffect(() => {
    loadModels();
    loadMetrics();
  }, []);

  const loadModels = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/models`);
      setModels(response.data);
    } catch (err) {
      console.error('Failed to load models:', err);
    }
  };

  const loadMetrics = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/metrics`);
      setMetrics(response.data);
    } catch (err) {
      console.error('Failed to load metrics:', err);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/api/v1/predict`, {
        customer: customerData,
      });
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setCustomerData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const metricsData = metrics?.metrics
    ? Object.entries(metrics.metrics).map(([name, value]) => ({
        name,
        value: (value * 100).toFixed(2),
      }))
    : [];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        ML Churn Prediction System
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tab} onChange={(e, v) => setTab(v)}>
          <Tab label="Prediction" />
          <Tab label="Models" />
          <Tab label="Metrics" />
        </Tabs>
      </Box>

      {tab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Customer Information
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Customer ID"
                    value={customerData.customer_id}
                    onChange={(e) => handleInputChange('customer_id', e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Age"
                    value={customerData.age}
                    onChange={(e) => handleInputChange('age', parseInt(e.target.value))}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Tenure (months)"
                    value={customerData.tenure}
                    onChange={(e) => handleInputChange('tenure', parseInt(e.target.value))}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Monthly Charges"
                    value={customerData.monthly_charges}
                    onChange={(e) => handleInputChange('monthly_charges', parseFloat(e.target.value))}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Total Charges"
                    value={customerData.total_charges}
                    onChange={(e) => handleInputChange('total_charges', parseFloat(e.target.value))}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    label="Contract Type"
                    value={customerData.contract_type}
                    onChange={(e) => handleInputChange('contract_type', e.target.value)}
                    SelectProps={{ native: true }}
                  >
                    <option value="Month-to-month">Month-to-month</option>
                    <option value="One year">One year</option>
                    <option value="Two year">Two year</option>
                  </TextField>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Payment Method"
                    value={customerData.payment_method}
                    onChange={(e) => handleInputChange('payment_method', e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    label="Internet Service"
                    value={customerData.internet_service}
                    onChange={(e) => handleInputChange('internet_service', e.target.value)}
                    SelectProps={{ native: true }}
                  >
                    <option value="DSL">DSL</option>
                    <option value="Fiber optic">Fiber optic</option>
                    <option value="No">No</option>
                  </TextField>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    label="Gender"
                    value={customerData.gender}
                    onChange={(e) => handleInputChange('gender', e.target.value)}
                    SelectProps={{ native: true }}
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </TextField>
                </Grid>
              </Grid>
              <Box sx={{ mt: 3 }}>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  onClick={handlePredict}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Predict Churn'}
                </Button>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Prediction Result
              </Typography>
              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
              {prediction && (
                <Box sx={{ mt: 2 }}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Churn Probability: {(prediction.probability * 100).toFixed(2)}%
                      </Typography>
                      <Typography variant="body1" color="text.secondary">
                        Prediction: {prediction.prediction === 1 ? 'Will Churn' : 'Will Not Churn'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Model Version: {prediction.model_version}
                      </Typography>
                      <Box sx={{ mt: 2, height: 200 }}>
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={[{ name: 'Churn Probability', value: prediction.probability * 100 }]}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis domain={[0, 100]} />
                            <Tooltip />
                            <Bar dataKey="value" fill="#8884d8" />
                          </BarChart>
                        </ResponsiveContainer>
                      </Box>
                    </CardContent>
                  </Card>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      )}

      {tab === 1 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Model Versions
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Version</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Traffic %</TableCell>
                  <TableCell>Created At</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {models.map((model) => (
                  <TableRow key={model.version}>
                    <TableCell>{model.version}</TableCell>
                    <TableCell>{model.model_type}</TableCell>
                    <TableCell>{model.status}</TableCell>
                    <TableCell>{model.traffic_percent}%</TableCell>
                    <TableCell>{new Date(model.created_at).toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {tab === 2 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Model Performance Metrics
          </Typography>
          {metrics && (
            <Box sx={{ mt: 2, height: 400 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={metricsData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          )}
        </Paper>
      )}
    </Container>
  );
}

export default App;


