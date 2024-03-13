import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Modal, Button, Form, Input, Card, Dropdown, Icon } from 'semantic-ui-react';

const RecommendationsContent = ({ setSearchResults, selectLocation }) => {
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
    { key: 'placeholder', value: '', text: 'Select State' },
    { key: 'al', value: 'Alabama', text: 'Alabama' },
    { key: 'me', value: 'Maine', text: 'Maine' },
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
    try {
      const queryParams = new URLSearchParams({
        user_id: 'user123',
        state: filters.state,
      });

      const url = `http://127.0.0.1:5000/api/recommendations?${queryParams}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Network response was not ok, status: ${response.status}`);

      const data = await response.json();
      if (data.error) {
        console.error(data.error);
        setLoading(false);
        return;
      }
      setSearchResultsLocal(data);
      setAllPoints(data);
      setSearchResults(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setLoading(false);
    }
}, [filters.state, setSearchResults]);


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
        <h2>Recommendations</h2>
        <div style={{ display: 'flex', flexDirection: 'column', marginBottom: '20px' }}>
          <Dropdown
            placeholder='Select State'
            fluid
            selection
            options={stateOptions}
            value={filters.state}
            onChange={(e, { value }) => setFilters(currentFilters => ({ ...currentFilters, state: value }))}
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

export default RecommendationsContent;
