import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Modal, Button, Form, Input, Card, Dropdown, Icon } from 'semantic-ui-react';

const SearchContent = ({ setSearchResults, selectLocation }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResultsLocal, setSearchResultsLocal] = useState([]);
  const [allPoints, setAllPoints] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [tempFilters, setTempFilters] = useState({ category: '', state: '', price: '' });
  const [filters, setFilters] = useState({ category: '', state: '', price: '' });
  const [tempRating, setTempRating] = useState(0);
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  const [selectedItemInfo, setSelectedItemInfo] = useState({});
  const resultsContainerRef = useRef(null);
  const [isRatingModalOpen, setIsRatingModalOpen] = useState(false);
  const [selectedForRating, setSelectedForRating] = useState(null);
  const [userRatings, setUserRatings] = useState({});

  const categoryOptions = [
    { key: '', value: '', text: 'All Categories' },
    { key: 'restaurant', value: 'restaurant', text: 'Restaurant' },
    { key: 'bar', value: 'bar', text: 'Bar' },
    { key: 'pub', value: 'pub', text: 'Pub' },
  ];

  const stateOptions = [
    { key: 'placeholder', value: '', text: 'Select State' }, // Placeholder option
    { key: 'al', value: 'Alabama', text: 'Alabama' },
    { key: 'ak', value: 'Alaska', text: 'Alaska' },
    { key: 'az', value: 'Arizona', text: 'Arizona' },
    { key: 'ar', value: 'Arkansas', text: 'Arkansas' },
    { key: 'ca', value: 'California', text: 'California' },
    { key: 'co', value: 'Colorado', text: 'Colorado' },
    { key: 'ct', value: 'Connecticut', text: 'Connecticut' },
    { key: 'de', value: 'Delaware', text: 'Delaware' },
    { key: 'fl', value: 'Florida', text: 'Florida' },
    { key: 'ga', value: 'Georgia', text: 'Georgia' },
    { key: 'hi', value: 'Hawaii', text: 'Hawaii' },
    { key: 'id', value: 'Idaho', text: 'Idaho' },
    { key: 'il', value: 'Illinois', text: 'Illinois' },
    { key: 'in', value: 'Indiana', text: 'Indiana' },
    { key: 'ia', value: 'Iowa', text: 'Iowa' },
    { key: 'ks', value: 'Kansas', text: 'Kansas' },
    { key: 'ky', value: 'Kentucky', text: 'Kentucky' },
    { key: 'la', value: 'Louisiana', text: 'Louisiana' },
    { key: 'me', value: 'Maine', text: 'Maine' },
    { key: 'md', value: 'Maryland', text: 'Maryland' },
    { key: 'ma', value: 'Massachusetts', text: 'Massachusetts' },
    { key: 'mi', value: 'Michigan', text: 'Michigan' },
    { key: 'mn', value: 'Minnesota', text: 'Minnesota' },
    { key: 'ms', value: 'Mississippi', text: 'Mississippi' },
    { key: 'mo', value: 'Missouri', text: 'Missouri' },
    { key: 'mt', value: 'Montana', text: 'Montana' },
    { key: 'ne', value: 'Nebraska', text: 'Nebraska' },
    { key: 'nv', value: 'Nevada', text: 'Nevada' },
    { key: 'nh', value: 'New Hampshire', text: 'New Hampshire' },
    { key: 'nj', value: 'New Jersey', text: 'New Jersey' },
    { key: 'nm', value: 'New Mexico', text: 'New Mexico' },
    { key: 'ny', value: 'New York', text: 'New York' },
    { key: 'nc', value: 'North Carolina', text: 'North Carolina' },
    { key: 'nd', value: 'North Dakota', text: 'North Dakota' },
    { key: 'oh', value: 'Ohio', text: 'Ohio' },
    { key: 'ok', value: 'Oklahoma', text: 'Oklahoma' },
    { key: 'or', value: 'Oregon', text: 'Oregon' },
    { key: 'pa', value: 'Pennsylvania', text: 'Pennsylvania' },
    { key: 'ri', value: 'Rhode Island', text: 'Rhode Island' },
    { key: 'sc', value: 'South Carolina', text: 'South Carolina' },
    { key: 'sd', value: 'South Dakota', text: 'South Dakota' },
    { key: 'tn', value: 'Tennessee', text: 'Tennessee' },
    { key: 'tx', value: 'Texas', text: 'Texas' },
    { key: 'ut', value: 'Utah', text: 'Utah' },
    { key: 'vt', value: 'Vermont', text: 'Vermont' },
    { key: 'va', value: 'Virginia', text: 'Virginia' },
    { key: 'wa', value: 'Washington', text: 'Washington' },
    { key: 'wv', value: 'West Virginia', text: 'West Virginia' },
    { key: 'wi', value: 'Wisconsin', text: 'Wisconsin' },
    { key: 'wy', value: 'Wyoming', text: 'Wyoming' },
  ];

  useEffect(() => {
    const handleScroll = (event) => {
      const { scrollTop, clientHeight, scrollHeight } = event.currentTarget;
      if (scrollHeight - scrollTop <= clientHeight + 100 && !loading) {
        setCurrentPage((prevPage) => prevPage + 1);
      }
    };

    const resultsContainer = resultsContainerRef.current;
    if (resultsContainer) {
      resultsContainer.addEventListener('scroll', handleScroll);
      return () => resultsContainer.removeEventListener('scroll', handleScroll);
    }
  }, [loading]);
  const prevFiltersRef = useRef({});

  useEffect(() => {
    prevFiltersRef.current = filters;
  });
  const fetchResults = useCallback(async () => {
    if (!filters.state) {
      setLoading(false);
      setSearchResultsLocal([]);
      setAllPoints([]);
      return; 
    }
    setLoading(true);
    const filtersChanged = JSON.stringify(filters) !== JSON.stringify(prevFiltersRef.current);
    try {
      const userId = 'user123';
      const queryParams = new URLSearchParams({
        name: searchTerm,
        category: filters.category,
        state: filters.state.toLowerCase(),  
        price: filters.price,
        page: currentPage,
        user_id: userId,
      });

      const url = `http://127.0.0.1:5000/api/placesfilter?${queryParams}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Network response was not ok, status: ${response.status}`);
      const data = await response.json();

      if (data.length === 0) {
        setLoading(false);
        return;
      }

      const newUserRatings = {};
      const updatedData = data.map((item) => {
        const userRating = item.rating === -1 ? 'You have not rated this place' : item.rating;
        newUserRatings[item.gmap_id] = userRating;

        return {
          ...item,
          userRating,
        };
      });

      setUserRatings(newUserRatings);

      if (currentPage === 1) {
        setSearchResultsLocal(updatedData);
        setAllPoints(updatedData);
      } else {
        const combinedData = [...searchResultsLocal, ...updatedData];
        setSearchResultsLocal(combinedData);
        setAllPoints(combinedData);
      }
      if (filtersChanged || currentPage === 1) {
        setSearchResultsLocal(updatedData); 
      } else {
        setSearchResultsLocal(prev => [...prev, ...updatedData]); 
      }
      setAllPoints(prev => filtersChanged || currentPage === 1 ? updatedData : [...prev, ...updatedData]);
      setSearchResults(prev => filtersChanged || currentPage === 1 ? updatedData : [...prev, ...updatedData]);

    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      setLoading(false);
    }
  }, [searchTerm, filters, currentPage]);
  useEffect(() => {
    fetchResults();
  }, [fetchResults]);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  const applyFilters = () => {
    setFilters(tempFilters);
    setOpen(false);
    setCurrentPage(1);
  };

  const handleCancel = () => {
    setTempFilters(filters);
    setOpen(false);
  };

  const ratePlace = (item) => {
    setSelectedForRating(item);
    setIsRatingModalOpen(true);
  };

  const showMoreInfo = (item) => {
    const descriptionToShow = item.description === -1 ? "Lack of Description" : item.description;

    setSelectedItemInfo({
      name: item.name,
      description: descriptionToShow
    });
    setIsInfoModalOpen(true);
  };

  const submitRating = async (rating) => {
    const payload = {
      gmap_id: selectedForRating.gmap_id,
      user_id: 'user123',
      rating: rating,
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/rate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json(); 
      setUserRatings((prevRatings) => ({
        ...prevRatings,
        [selectedForRating.gmap_id]: rating,
      }));

      const updatedSearchResultsLocal = searchResultsLocal.map(item => {
        if (item.gmap_id === selectedForRating.gmap_id) {
          return { ...item, userRating: rating };
        }
        return item;
      });

      setSearchResultsLocal(updatedSearchResultsLocal); 

      setIsRatingModalOpen(false);
      setTempRating(0); 
    } catch (error) {
      console.error("Error submitting rating:", error);
    }
  };


  const centerMapOnObject = (latitude, longitude) => {
    selectLocation(latitude, longitude);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ padding: '20px' }}>
        <h2>Search</h2>
        <div style={{ display: 'flex', flexDirection: 'column', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
            <Input
              icon='search'
              placeholder='Search...'
              value={searchTerm}
              onChange={handleSearch}
              style={{ flex: 1, marginRight: '10px' }}
            />
            <Button icon="filter" onClick={() => setOpen(true)}></Button>
          </div>
          <Dropdown
            placeholder='Select State'
            fluid
            selection
            options={stateOptions}
            value={filters.state}
            onChange={(e, { value }) => setFilters({ ...filters, state: value })}
            style={{ marginBottom: '10px' }}
          />
          {!filters.state && <span>Choose a state to see locals.</span>}
        </div>
      </div>
      <Modal open={open} onClose={handleCancel} size="small" header="Filter Options">
        <Modal.Content>
          <Form>
            <Form.Field>
              <label>Category</label>
              <Dropdown placeholder="Select Category" fluid selection options={categoryOptions} value={tempFilters.category} onChange={(e, { value }) => setTempFilters({ ...tempFilters, category: value })} />
            </Form.Field>
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={handleCancel}>Cancel</Button>
          <Button positive onClick={applyFilters}>Apply Filters</Button>
        </Modal.Actions>
      </Modal>
      <Modal open={isInfoModalOpen} onClose={() => setIsInfoModalOpen(false)} size="small">
        <Modal.Header>{selectedItemInfo.name}</Modal.Header>
        <Modal.Content>
          <p>{selectedItemInfo.description}</p> {}
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setIsInfoModalOpen(false)}>Close</Button>
        </Modal.Actions>
      </Modal>
      <Modal open={isRatingModalOpen} onClose={() => { setIsRatingModalOpen(false); setTempRating(0); }}>
        <Modal.Header>Rate {selectedForRating?.name}</Modal.Header>
        <Modal.Content>
          <div>Select your rating:</div>
          <div>
            {[1, 2, 3, 4, 5].map((rating) => (
              <Icon key={rating} name={tempRating >= rating ? "star" : "star outline"} color={tempRating >= rating ? "yellow" : "grey"} onClick={() => setTempRating(rating)} style={{ cursor: 'pointer' }} />
            ))}
          </div>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => { setIsRatingModalOpen(false); setTempRating(0); }}>Cancel</Button>
          <Button onClick={() => { submitRating(tempRating); setIsRatingModalOpen(false); setTempRating(0); }} positive>Submit</Button>
        </Modal.Actions>
      </Modal>
      <div ref={resultsContainerRef} className="results-container" style={{ flexGrow: 1, overflowY: 'auto', maxHeight: 'calc(100vh - 160px)' }}>
      {searchResultsLocal.map((result, index) => (
        <Card key={index} style={{ width: '100%', marginBottom: '10px' }}>
          <Card.Content>
            <Card.Header style={{ wordWrap: 'break-word' }}>{result.name}</Card.Header>
            <Card.Meta>
              {}
              <span className='date'>{`Category: ${result.category} - Rating: ${result.avg_rating} (${result.num_of_reviews} reviews)`}</span>
            </Card.Meta>
            <Card.Description style={{ wordWrap: 'break-word', color: result.userRating !== 'You have not rated this place' ? 'blue' : 'black' }}>
              {typeof result.userRating === 'number' ? `Your rating: ${result.userRating}` : result.userRating}
            </Card.Description>
            <div style={{ marginTop: '10px' }}>
              <Button icon onClick={() => ratePlace(result)}>
                <Icon name="star" color={result.user_has_rated ? 'yellow' : null} />
              </Button>
              <Button icon onClick={() => centerMapOnObject(result.latitude, result.longitude)}>
                <Icon name="location arrow" />
              </Button>
              <Button onClick={() => showMoreInfo(result)}>More Info</Button>
            </div>
          </Card.Content>
        </Card>
      ))}
      {loading && <p>Loading more results...</p>}
    </div>

    </div>
  );
};

export default SearchContent;
