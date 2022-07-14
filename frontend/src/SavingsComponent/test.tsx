import React from 'react';
import { render, screen } from '@testing-library/react';
import SavingsComponent from '.';

test('renders learn react link', () => {
  render(<SavingsComponent />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
